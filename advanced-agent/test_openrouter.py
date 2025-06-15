import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

def test_openrouter():
    print("🧪 Testing OpenRouter connection...")
    
    # Check API key first
    api_key = "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"
    base_url = "https://openrouter.ai/api/v1"
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment!")
        return False
    
    print(f"💡 API Key found (first 10 chars): {api_key[:10]}...")
    
    try:
        # Create prompt template
        template = """Question: {question}
Answer: Let's think step by step."""
        
        prompt = PromptTemplate(template=template, input_variables=["question"])
        
        # Initialize OpenRouter model with streaming enabled
        llm = ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base=base_url,
            model_name="qwen/qwen2.5-vl-32b-instruct:free",
            streaming=True
        )
        
        # Create modern chain using RunnableSequence
        chain = prompt | llm
        
        # Test question
        question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
        
        print("🔄 Sending test message to OpenRouter...")
        print("📝 Streaming Response:")
        print("-" * 50)
        
        # Stream the response
        full_response = ""
        for chunk in chain.stream({"question": question}):
            if chunk.content:
                print(chunk.content, end="", flush=True)
                full_response += chunk.content
        
        print("\n" + "-" * 50)
        print("✅ SUCCESS! OpenRouter streaming is working!")
        
        return True
        
    except Exception as e:
        print("❌ FAILED! OpenRouter connection failed!")
        print(f"🚨 Error: {str(e)}")
        
        # Additional debugging
        if "401" in str(e):
            print("💡 This is an authentication error. Possible issues:")
            print("   - API key might be invalid or expired")
            print("   - Check if your OpenRouter account has credits")
        
        return False

if __name__ == "__main__":
    print("🚀 Starting OpenRouter streaming test...\n")
    test_openrouter()
    print("\n🏁 Test completed!") 