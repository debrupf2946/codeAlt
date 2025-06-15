import os
import time
from firecrawl import FirecrawlApp,ScrapeOptions
from dotenv import load_dotenv
from .logger_config import get_logger

load_dotenv()

# Create logger for this module
logger = get_logger(__name__)

class FireCrawlService:
    def __init__(self):
        logger.info("🔥 Initializing FireCrawl service")
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            logger.error("❌ Missing FIRECRAWL_API_KEY environment variable")
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        
        logger.debug(f"Using FireCrawl API key: {api_key[:10]}...")
        self.app = FirecrawlApp(api_key="fc-b99646672e6c4320b081caac8da3f6c3")
        logger.info("✅ FireCrawl service initialized successfully")

    def search_companies(self, query: str, num_results: int = 5):
        logger.info(f"🔍 Searching for companies with query: '{query}', limit: {num_results}")
        try:
            result = self.app.search(
                query=f"{query} company pricing",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            logger.info(f"✅ Found {len(result.data) if result.data else 0} results")
            return result
        except Exception as e:
            logger.error(f"❌ Error searching companies: {e}")
            return []

    def scrape_company_pages(self, url: str):
        logger.info(f"📄 Scraping URL: {url}")
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"]
            )
            logger.info(f"✅ Successfully scraped {url}")
            return result
        except Exception as e:
            logger.error(f"❌ Error scraping URL {url}: {e}")
            return None
        
        
            
        




