from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

print("FIRECRAWL_API_KEY:", os.getenv("FIRECRAWL_API_KEY"))

model = ChatOllama(model="qwen3:8b",temperature=0.0,base_url="https://f6b9-34-16-163-131.ngrok-free.app/")

server_params = StdioServerParameters(
    command="npx",
    env={"FIRECRAWL_API_KEY":os.getenv("FIRECRAWL_API_KEY")},
    args=["firecrawl-mcp"]
    
)

async def main():
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            
            tools= await load_mcp_tools(session)
            agent = create_react_agent(model,tools)
            
            
            messages = [
                {"role":"system",
                 "content":"You are a helpful assistant that can scrape websites, crawl pages, and extract data using Firecrawl tools. Think step by step and use the appropriate tools to help the user."
                }
            ]
            
            print("available tools-:",*[tool.name for tool in tools])
            print("-"*60)
            
            while True:
                user_input = input("Enter your query:")
                if user_input.lower() in ["exit","quit","bye"]:
                    print("Exiting...")
                    break
                messages.append({"role":"user","content":user_input[:175000]})
                
                
                try:
                    agent_response = await agent.ainvoke({"messages":messages})
                    ai_message = agent_response["messages"][-1].content
                    print("AGENT:",ai_message)
                except Exception as e:
                    print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

            
            
            



# if __name__ == "__main__":
#     main()
