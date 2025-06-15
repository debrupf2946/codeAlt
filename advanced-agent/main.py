from dotenv import load_dotenv
from src.workflow import Workflow
from src.logger_config import get_logger

load_dotenv()

# Create a logger for this module
logger = get_logger(__name__)


def main():
    logger.info("🚀 Starting Developer Tools Research Agent")
    workflow = Workflow()
    logger.info("Developer Tools Research Agent initialized")

    while True:
        query = input("\n🔍 Developer Tools Query: ").strip()
        if query.lower() in {"quit", "exit"}:
            logger.info("👋 User requested to quit")
            break

        if query:
            logger.info(f"📋 Processing query: '{query}'")
            result = workflow.run(query)
            logger.info(f"✅ Query processed successfully, found {len(result.companies)} companies")
            
            print(f"\n📊 Results for: {query}")
            print("=" * 60)

            for i, company in enumerate(result.companies, 1):
                logger.debug(f"Displaying results for company: {company.name}")
                print(f"\n{i}. 🏢 {company.name}")
                print(f"   🌐 Website: {company.website}")
                print(f"   💰 Pricing: {company.pricing_model}")
                print(f"   📖 Open Source: {company.is_open_source}")

                if company.tech_stack:
                    print(f"   🛠️  Tech Stack: {', '.join(company.tech_stack[:5])}")

                if company.language_support:
                    print(
                        f"   💻 Language Support: {', '.join(company.language_support[:5])}"
                    )

                if company.api_available is not None:
                    api_status = (
                        "✅ Available" if company.api_available else "❌ Not Available"
                    )
                    print(f"   🔌 API: {api_status}")

                if company.integration_capabilities:
                    print(
                        f"   🔗 Integrations: {', '.join(company.integration_capabilities[:4])}"
                    )

                if company.description and company.description != "Analysis failed":
                    print(f"   📝 Description: {company.description}")

                print()

            if result.analysis:
                logger.debug("Displaying final analysis and recommendations")
                print("Developer Recommendations: ")
                print("-" * 40)
                print(result.analysis)
        else:
            logger.warning("⚠️ Empty query received, skipping...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("👋 Application interrupted by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error occurred: {e}")
        raise