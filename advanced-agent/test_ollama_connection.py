#!/usr/bin/env python3
"""
Simple test script to check Ollama connection
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import sys
import time

def test_ollama_connection():
    """Test if Ollama connection is working"""
    
    print("🔍 Testing Ollama connection...")
    print("=" * 50)
    
    # Configuration from workflow.py
    model_name = "qwen3:14b"
    ollama_url = "https://acba-34-124-238-213.ngrok-free.app/"
    
    print(f"Model: {model_name}")
    print(f"URL: {ollama_url}")
    print("-" * 50)
    
    try:
        # Initialize the ChatOllama client
        print("🚀 Initializing ChatOllama client...")
        llm = ChatOllama(
            model=model_name,
            temperature=0.0,
            base_url=ollama_url
        )
        
        # Test with a simple message
        print("📝 Sending test message...")
        test_message = HumanMessage(content="Hello! Can you respond with just 'Connection successful'?")
        
        # Set a timeout for the request
        start_time = time.time()
        response = llm.invoke([test_message])
        end_time = time.time()
        
        # Success!
        print("✅ CONNECTION SUCCESSFUL!")
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Response: {response.content}")
        
        return True
        
    except ConnectionError as e:
        print("❌ CONNECTION ERROR!")
        print(f"Error: {e}")
        print("💡 Check if:")
        print("   - Ollama server is running")
        print("   - The URL is correct and accessible")
        print("   - Network connectivity is working")
        return False
        
    except Exception as e:
        print("❌ UNEXPECTED ERROR!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        
        # Check for specific error types
        if "Connection refused" in str(e):
            print("💡 This looks like a connection refused error.")
            print("   - Make sure Ollama is running on the specified URL")
            print("   - Check if the ngrok tunnel is active")
        elif "timeout" in str(e).lower():
            print("💡 This looks like a timeout error.")
            print("   - The server might be slow to respond")
            print("   - Try increasing the timeout or check server load")
        
        return False

def test_basic_connectivity():
    """Test basic network connectivity to the Ollama URL"""
    import requests
    
    print("\n🌐 Testing basic network connectivity...")
    print("=" * 50)
    
    ollama_url = "https://acba-34-124-238-213.ngrok-free.app/"
    
    try:
        # Test basic HTTP connectivity
        response = requests.get(ollama_url, timeout=10)
        print(f"✅ HTTP connection successful! Status code: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Cannot reach the URL - Connection refused")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Network error: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Ollama Connection Test")
    print("=" * 50)
    
    # Test basic connectivity first
    network_ok = test_basic_connectivity()
    
    if network_ok:
        # Test Ollama connection
        ollama_ok = test_ollama_connection()
        
        if ollama_ok:
            print("\n🎉 ALL TESTS PASSED!")
            print("Your Ollama connection is working properly.")
            sys.exit(0)
        else:
            print("\n❌ OLLAMA CONNECTION FAILED!")
            sys.exit(1)
    else:
        print("\n❌ NETWORK CONNECTION FAILED!")
        print("Cannot reach the Ollama server URL.")
        sys.exit(1) 