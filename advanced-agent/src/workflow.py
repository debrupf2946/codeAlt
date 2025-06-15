import os
from typing import List,Dict,Any
from src.models import CompanyInfo,CompanyAnalysis,ResearchState
from src.prompts import DeveloperToolsPrompts
from src.firecrawl import FireCrawlService
from src.logger_config import get_logger
from langgraph.graph import StateGraph,END
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage
from dotenv import load_dotenv


load_dotenv()

# Create logger for this module
logger = get_logger(__name__)

class Workflow:
    def __init__(self):
        logger.info("🚀 Initializing Workflow")
        self.firecrawl_service = FireCrawlService()
        self.llm = ChatOpenAI(
            openai_api_key="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",
            openai_api_base="https://openrouter.ai/api/v1",
            model_name="qwen/qwen3-14b:free",
        )
        self.prompt = DeveloperToolsPrompts()
        self.workflow = self._build_workflow()
        logger.info("✅ Workflow initialized successfully")
        
        
    def _build_workflow(self):
        logger.debug("🔧 Building workflow graph")
        graph = StateGraph(ResearchState)
        
        graph.add_node("extract_tools",self._extract_tools)
        graph.add_node("analyze_companies",self._analyze_step)
        graph.add_node("research_step",self._research_step)
        
        graph.set_entry_point("extract_tools")
        graph.add_edge("extract_tools","research_step")
        graph.add_edge("research_step","analyze_companies")
        graph.add_edge("analyze_companies",END)
        
        logger.debug("✅ Workflow graph built successfully")
        return graph.compile()
        
        
        
        
        
    
    def _extract_tools(self, state:ResearchState)->Dict[str,Any]:
        
        logger.info(f"🔍 Finding articles about: {state.query}")
        article_query =f"{state.query} tools comparison best alternatives"
        
        search_results = self.firecrawl_service.search_companies(article_query,num_results=3)
        
        all_content = ""
        for result in search_results.data:
            url = result.get("url","")
            content = self.firecrawl_service.scrape_company_pages(url)
            if content:
                all_content += content.markdown[:1500] + "\n\n"
                
                
        messages = [
            SystemMessage(content=self.prompt.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompt.tool_extraction_user(state.query, all_content))
        ]
        try:
            response = self.llm.invoke(messages)
            tool_names= [names.strip() for names in response.content.strip().split("\n") if names.strip()]
            
            logger.info(f"✅ Extracted tools: {', '.join(tool_names[:5])}")
            return {"extracted_tools": tool_names}
        except Exception as e:
            logger.error(f"❌ Error extracting tools: {e}")
            return {"extracted_tools": []}
        
        
    def _analyze_company_content(self,company_name:str,content:str)->CompanyAnalysis:
        logger.debug(f"🔍 Analyzing content for company: {company_name}")
        
        structured_llm =self.llm.with_structured_output(CompanyAnalysis)
        
        messages = [
            SystemMessage(content=self.prompt.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompt.tool_analysis_user(company_name,content))
        ]
        
        
        try:
            response = structured_llm.invoke(messages)
            logger.debug(f"✅ Successfully analyzed {company_name}")
            return response
        except Exception as e:
            logger.error(f"❌ Error analyzing company content for {company_name}: {e}")
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                description="Failed to analyze company content",
                api_available=None,
                language_support=[],
                integration_capabilities=[]
            )
        
        
        
    def _research_step(self,state:ResearchState)->Dict[str,Any]:
        
        extracted_tools = getattr(state, "extracted_tools", [])
        
        if not extracted_tools:
            logger.warning("⚠️ No extracted tools found, falling back to direct search")
            search_results = self.firecrawl_service.search_companies(f"{state.query} tools comparison best alternatives",num_results=3)
            tool_names = [result.get("metadata", {}).get("title", "Unknown") for result in search_results.data]
            
        else:
            tool_names = extracted_tools[:4]
            
        logger.info(f"🔬 Researching specific tools: {', '.join(tool_names)}")
        
        companies=[]
        for tool in tool_names:
            logger.info(f"🔍 Analyzing company: {tool}")
            tool_search_result= self.firecrawl_service.search_companies(tool + " official site", num_results=1)
            
            if tool_search_result:
                result = tool_search_result.data[0]
                url = result.get("url","")
                
                
                
                company=CompanyInfo(
                    name=tool,
                    description=result.get("markdown",""),
                    website=url,
                    tech_stack=[],
                    competitors=[],
                )
                
                scraped_content = self.firecrawl_service.scrape_company_pages(url)
                if scraped_content:
                    content = scraped_content.markdown
                    analysis = self._analyze_company_content(company.name,content)
                    
                    company.pricing_model = analysis.pricing_model
                    company.is_open_source = analysis.is_open_source
                    company.tech_stack = analysis.tech_stack
                    company.description = analysis.description
                    company.api_available = analysis.api_available
                    company.language_support = analysis.language_support
                    company.integration_capabilities = analysis.integration_capabilities
                    
                companies.append(company)
                
        logger.info(f"✅ Completed research for {len(companies)} companies")
        return {"companies":companies}
        
        
        
    def _analyze_step(self,state:ResearchState)->Dict[str,Any]:
        
        logger.info("🔍 Analyzing companies")
        
        company_data=",".join([company.json() for company in state.companies])
        
        messages = [
            SystemMessage(content=self.prompt.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompt.recommendations_user(state.query,company_data))
        ]
        
        # Add retry logic for API failures
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = self.llm.invoke(messages)
                logger.info("✅ Company analysis completed")
                return {"analysis":response.content}
            except Exception as e:
                logger.warning(f"⚠️ API call failed (attempt {attempt + 1}/{max_retries}): {e}")
                
                if attempt == max_retries - 1:
                    # Last attempt failed, return a fallback response
                    logger.error(f"❌ All API attempts failed. Providing fallback analysis.")
                    fallback_analysis = f"""
                    Analysis temporarily unavailable due to API issues.
                    
                    Found {len(state.companies)} companies for query: {state.query}
                    
                    Companies analyzed:
                    {chr(10).join([f"- {company.name}: {company.website}" for company in state.companies])}
                    
                    Please try again later for detailed analysis.
                    """
                    return {"analysis": fallback_analysis}
                
                # Wait before retrying
                import time
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
    
    
    def run(self,query:str)->ResearchState:
        logger.info(f"🚀 Starting workflow run for query: '{query}'")
        
        initial_state = ResearchState(query=query)
        
        final_state = self.workflow.invoke(initial_state)
        logger.info("✅ Workflow run completed successfully")
        
        return ResearchState(**final_state)
    
            

            
                    

                    
                    
                    
                    
                    
                

                
                
                

            
            
            


        
        
        
        
        
