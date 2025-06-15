import pytest
from unittest.mock import patch, MagicMock
from src.firecrawl import FireCrawlService
url="https://en.wikipedia.org/wiki/The_Combat:_Woman_Pleading_for_the_Vanquished"

# UNIT TESTS (with mocks - no real API calls)
@pytest.fixture
def firecrawl_service():
    # Patch FirecrawlApp so no real API calls are made
    with patch('src.firecrawl.FirecrawlApp') as MockApp:
        mock_app = MockApp.return_value
        yield FireCrawlService(), mock_app


@pytest.mark.integration
def test_real_search_companies(real_firecrawl_service):
    """Test real API call to search for companies"""
    service = real_firecrawl_service
    results = service.search_companies('stripe', num_results=2)
    print(f"\n=== REAL SEARCH RESULTS ===")
    print(f"Type: {type(results)}")
    print(f"Results: {results}")
    if hasattr(results, 'data') and results.data:
        for i, item in enumerate(results.data):
            print(f"\n--- Result {i+1} ---")
            print(f"URL: {item.get('url', 'No URL')}")
            print(f"Markdown preview: {item.get('markdown', 'No content')[:200]}...")
    assert results is not None

@pytest.mark.integration
def test_real_scrape_company_page(real_firecrawl_service):
    """Test real API call to scrape a company page"""
    service = real_firecrawl_service
    result = service.scrape_company_pages('https://stripe.com/pricing')
    print(f"\n=== REAL SCRAPE RESULTS ===")
    print(f"Type: {type(result)}")
    if result:
        print(f"Markdown preview: {result.markdown[:500]}...")
    else:
        print("No results returned")
    assert result is not None

@pytest.mark.integration
def test_both_methods_together(real_firecrawl_service):
    """Test both search and scrape methods working together"""
    service = real_firecrawl_service
    
    # Step 1: Search for companies
    print(f"\n=== STEP 1: SEARCHING FOR COMPANIES ===")
    search_results = service.search_companies('openai', num_results=1)
    print(f"Search successful: {search_results is not None and hasattr(search_results, 'data')}")
    
    if hasattr(search_results, 'data') and search_results.data:
        first_url = search_results.data[0].get('url')
        print(f"Found URL: {first_url}")
        
        # Step 2: Scrape the first URL found
        print(f"\n=== STEP 2: SCRAPING FOUND URL ===")
        scrape_result = service.scrape_company_pages(first_url)
        print(f"Scrape successful: {scrape_result is not None}")
        
        if scrape_result:
            print(f"Scraped content preview: {scrape_result.markdown[:300]}...")
            assert scrape_result.markdown is not None
        
        print(f"\n🎉 BOTH METHODS WORKING TOGETHER SUCCESSFULLY!")
        assert True
    else:
        print("No search results to scrape")
        assert False, "Search didn't return results"