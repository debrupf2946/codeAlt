"""
Example usage of the LLM Factory Design Pattern

This file demonstrates different ways to use the factory pattern to create LLM models.
"""

from llm_models.llm_factory import ModelFactory, LLMFactoryRegistry, ModelType


def main():
    """Demonstrate various ways to use the factory pattern"""
    
    print("=== LLM Factory Pattern Usage Examples ===\n")
    
    # Method 1: Using the simple ModelFactory (Recommended for most cases)
    print("1. Using ModelFactory (Simple approach):")
    try:
        # Create different models using the simple factory
        ollama_model = ModelFactory.create_model(
            model_type="ollama",
            model_name="llama2",
            temperature=0.1,
            base_url="http://localhost:11434"
        )
        print(f"✓ Created Ollama model: {type(ollama_model).__name__}")
        
        groq_model = ModelFactory.create_model(
            model_type="groq",
            model_name="mixtral-8x7b-32768",
            temperature=0.2
        )
        print(f"✓ Created Groq model: {type(groq_model).__name__}")
        
        gemini_model = ModelFactory.create_model(
            model_type="gemini",
            model_name="gemini-pro",
            temperature=0.0
        )
        print(f"✓ Created Gemini model: {type(gemini_model).__name__}")
        
    except ValueError as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Method 2: Using LLMFactoryRegistry with ModelType enum (Type-safe approach)
    print("2. Using LLMFactoryRegistry with ModelType enum:")
    try:
        # Create models using the registry with enum types
        ollama_model = LLMFactoryRegistry.create_model(
            ModelType.OLLAMA,
            "codellama",
            temperature=0.0
        )
        print(f"✓ Created Ollama model: {type(ollama_model).__name__}")
        
        groq_model = LLMFactoryRegistry.create_model(
            ModelType.GROQ,
            "llama2-70b-4096",
            temperature=0.3
        )
        print(f"✓ Created Groq model: {type(groq_model).__name__}")
        
    except ValueError as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Method 3: Using individual factories (Advanced usage)
    print("3. Using individual factories:")
    try:
        # Get specific factory and create model
        ollama_factory = LLMFactoryRegistry.get_factory(ModelType.OLLAMA)
        ollama_model = ollama_factory.create_model(
            "phi",
            temperature=0.5,
            base_url="http://custom-ollama:11434"
        )
        print(f"✓ Created Ollama model with custom factory: {type(ollama_model).__name__}")
        
    except ValueError as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Method 4: Error handling and supported types
    print("4. Error handling and supported types:")
    
    # Show supported types
    supported_types = ModelFactory.get_supported_types()
    print(f"Supported model types: {supported_types}")
    
    # Try to create an unsupported model type
    try:
        invalid_model = ModelFactory.create_model("openai", "gpt-4")
        print(f"✓ Created model: {type(invalid_model).__name__}")
    except ValueError as e:
        print(f"✗ Expected error for unsupported type: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Method 5: Extending the factory (Adding new model types)
    print("5. Extending the factory pattern:")
    print("To add a new model type, you would:")
    print("  a. Create a new model class inheriting from LLMModel")
    print("  b. Create a new factory class inheriting from LLMFactory")  
    print("  c. Add the model type to ModelType enum")
    print("  d. Register the factory in LLMFactoryRegistry._factories")
    print("  e. Or use LLMFactoryRegistry.register_factory() at runtime")


def demonstrate_actual_model_usage():
    """Demonstrate how to actually use the created models"""
    print("=== Using Created Models ===\n")
    
    try:
        # Create a model
        model_wrapper = ModelFactory.create_model(
            model_type="ollama",
            model_name="llama2",
            temperature=0.1
        )
        
        # Get the actual LangChain model
        langchain_model = model_wrapper.get_model()
        print(f"✓ Created LangChain model: {type(langchain_model).__name__}")
        
        # You can now use this model with LangChain
        # response = langchain_model.invoke("Hello, how are you?")
        # print(f"Model response: {response}")
        
    except Exception as e:
        print(f"✗ Error creating model: {e}")


if __name__ == "__main__":
    main()
    print("\n")
    demonstrate_actual_model_usage() 