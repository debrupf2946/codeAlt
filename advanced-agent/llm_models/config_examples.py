"""
Configuration Examples for LLM Models

This file demonstrates various ways to configure and create LLM models
with different configuration requirements.
"""

import os
from llm_models.config import (
    ConfigManager, EnvironmentConfigLoader,
    OllamaConfig, GroqConfig, GeminiConfig, OpenRouterConfig
)
from llm_models.llm_factory import ModelFactory


def demonstrate_config_creation():
    """Show different ways to create configurations"""
    print("=== Configuration Creation Examples ===\n")
    
    # 1. Create configurations directly
    print("1. Creating configurations directly:")
    
    # Ollama config (minimal requirements)
    ollama_config = OllamaConfig(
        model_name="llama2",
        temperature=0.1,
        base_url="http://localhost:11434"
    )
    print(f"✓ Ollama config: {ollama_config}")
    
    # Groq config (requires API key)
    groq_config = GroqConfig(
        model_name="mixtral-8x7b-32768",
        temperature=0.2,
        api_key="your-groq-api-key",  # In practice, use environment variable
        max_retries=3
    )
    print(f"✓ Groq config: {groq_config}")
    
    # Gemini config (requires API key)
    gemini_config = GeminiConfig(
        model_name="gemini-pro",
        temperature=0.0,
        api_key="your-google-api-key"  # In practice, use environment variable
    )
    print(f"✓ Gemini config: {gemini_config}")
    
    # OpenRouter config (complex requirements)
    openrouter_config = OpenRouterConfig(
        model_name="openai/gpt-4",
        temperature=0.1,
        api_key="your-openrouter-api-key",  # In practice, use environment variable
        app_url="https://myapp.com",
        app_title="My AI Agent"
    )
    print(f"✓ OpenRouter config: {openrouter_config}")
    
    print("\n" + "="*60 + "\n")


def demonstrate_config_manager():
    """Show how to use ConfigManager for validation and creation"""
    print("2. Using ConfigManager for validated configuration:")
    
    try:
        # Create configs using ConfigManager (with validation)
        ollama_config = ConfigManager.create_config(
            "ollama",
            model_name="codellama",
            temperature=0.0,
            base_url="http://custom-ollama:11434"
        )
        print(f"✓ Valid Ollama config created: {ollama_config.model_name}")
        
        # Try to create invalid config
        try:
            invalid_config = ConfigManager.create_config(
                "groq",
                model_name="mixtral-8x7b-32768"
                # Missing required api_key
            )
        except ValueError as e:
            print(f"✓ Caught expected validation error: {str(e).split(':')[0]}")
            
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    print("\n" + "="*60 + "\n")


def demonstrate_environment_config():
    """Show how to use environment variables for configuration"""
    print("3. Using environment variables for configuration:")
    
    # Set some example environment variables
    os.environ.update({
        "OLLAMA_TEMPERATURE": "0.2",
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "GROQ_API_KEY": "fake-groq-key-for-demo",
        "GROQ_TEMPERATURE": "0.3",
        "GOOGLE_API_KEY": "fake-google-key-for-demo",
        "OPENROUTER_API_KEY": "fake-openrouter-key-for-demo",
        "APP_URL": "https://demo-app.com",
        "APP_TITLE": "Demo Agent"
    })
    
    try:
        # Load configurations from environment
        ollama_config = EnvironmentConfigLoader.load_config("ollama", "llama2")
        print(f"✓ Ollama from env: temp={ollama_config.temperature}, url={ollama_config.base_url}")
        
        groq_config = EnvironmentConfigLoader.load_config("groq", "mixtral-8x7b-32768")
        print(f"✓ Groq from env: temp={groq_config.temperature}, key={'***' + groq_config.api_key[-4:]}")
        
        openrouter_config = EnvironmentConfigLoader.load_config("openrouter", "openai/gpt-4")
        print(f"✓ OpenRouter from env: title={openrouter_config.app_title}, url={openrouter_config.app_url}")
        
    except Exception as e:
        print(f"✗ Error loading from environment: {e}")
    
    print("\n" + "="*60 + "\n")


def demonstrate_factory_with_configs():
    """Show how to use the factory with different configuration methods"""
    print("4. Using ModelFactory with different configuration approaches:")
    
    # Set up environment for this demo
    os.environ.update({
        "GROQ_API_KEY": "demo-groq-key",
        "GOOGLE_API_KEY": "demo-google-key",
        "OPENROUTER_API_KEY": "demo-openrouter-key"
    })
    
    try:
        # Method 1: Direct parameters (simple)
        print("Method 1: Direct parameters")
        model1 = ModelFactory.create_model(
            "ollama", 
            "llama2", 
            temperature=0.1, 
            base_url="http://localhost:11434"
        )
        print(f"✓ Created {type(model1).__name__} with direct params")
        
        # Method 2: Using configuration objects (type-safe)
        print("Method 2: Configuration objects")
        config = GroqConfig(
            model_name="mixtral-8x7b-32768",
            temperature=0.2,
            api_key="demo-key"
        )
        model2 = ModelFactory.create_model_with_config(config)
        print(f"✓ Created {type(model2).__name__} with config object")
        
        # Method 3: From environment variables (secure)
        print("Method 3: Environment variables")
        model3 = ModelFactory.create_model_from_env("groq", "llama2-70b-4096")
        print(f"✓ Created {type(model3).__name__} from environment")
        
        # Method 4: From dictionary (flexible)
        print("Method 4: Dictionary configuration")
        config_dict = {
            "model_type": "gemini",
            "model_name": "gemini-pro",
            "temperature": 0.0,
            "api_key": "demo-key"
        }
        model4 = ModelFactory.create_model_from_dict(config_dict)
        print(f"✓ Created {type(model4).__name__} from dictionary")
        
    except Exception as e:
        print(f"✗ Error creating models: {e}")
    
    print("\n" + "="*60 + "\n")


def demonstrate_json_config():
    """Show how to use JSON configuration files"""
    print("5. Using JSON configuration files:")
    
    # Create example JSON config
    json_config = {
        "development": {
            "model_type": "ollama",
            "model_name": "llama2",
            "temperature": 0.1,
            "base_url": "http://localhost:11434"
        },
        "production": {
            "model_type": "groq",
            "model_name": "mixtral-8x7b-32768",
            "temperature": 0.0,
            "api_key": "your-production-key"
        },
        "research": {
            "model_type": "openrouter",
            "model_name": "anthropic/claude-3-opus",
            "temperature": 0.3,
            "api_key": "your-openrouter-key",
            "app_title": "Research Agent"
        }
    }
    
    # Write to file
    import json
    config_file = "model_configs.json"
    with open(config_file, 'w') as f:
        json.dump(json_config, f, indent=2)
    
    try:
        # Load and create model from JSON
        model = ModelFactory.create_model_from_json(config_file, "development")
        print(f"✓ Created {type(model).__name__} from JSON config file")
        
        # Clean up
        os.remove(config_file)
        
    except Exception as e:
        print(f"✗ Error with JSON config: {e}")
        # Clean up on error
        if os.path.exists(config_file):
            os.remove(config_file)
    
    print("\n" + "="*60 + "\n")


def demonstrate_config_validation():
    """Show configuration validation in action"""
    print("6. Configuration validation examples:")
    
    # Test various validation scenarios
    test_cases = [
        {
            "name": "Missing model name",
            "type": "ollama",
            "config": {"temperature": 0.1}
        },
        {
            "name": "Invalid temperature", 
            "type": "groq",
            "config": {"model_name": "mixtral", "temperature": -1}
        },
        {
            "name": "Missing API key",
            "type": "groq", 
            "config": {"model_name": "mixtral", "temperature": 0.1}
        },
        {
            "name": "Valid configuration",
            "type": "ollama",
            "config": {"model_name": "llama2", "temperature": 0.1}
        }
    ]
    
    for test_case in test_cases:
        try:
            config = ConfigManager.create_config(test_case["type"], **test_case["config"])
            print(f"✓ {test_case['name']}: Valid")
        except ValueError as e:
            print(f"✗ {test_case['name']}: {str(e).split(':')[0]}")
    
    print("\n" + "="*60 + "\n")


def main():
    """Run all configuration examples"""
    print("=== LLM Configuration System Examples ===\n")
    
    demonstrate_config_creation()
    demonstrate_config_manager()
    demonstrate_environment_config()
    demonstrate_factory_with_configs()
    demonstrate_json_config()
    demonstrate_config_validation()
    
    print("=== Best Practices Summary ===")
    print("1. Use environment variables for sensitive data (API keys)")
    print("2. Use configuration objects for type safety and validation")
    print("3. Use JSON files for complex multi-environment setups")
    print("4. Always validate configurations before using them")
    print("5. Handle different model requirements gracefully")


if __name__ == "__main__":
    main() 