from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Type, Optional, Any
from .model import LLMModel, OllamaModel, GroqModel, GeminiModel, OpenRouterModel
from .config import (
    ConfigManager, EnvironmentConfigLoader, BaseModelConfig,
    OllamaConfig, GroqConfig, GeminiConfig, OpenRouterConfig
)


class ModelType(Enum):
    """Enum for supported model types"""
    OLLAMA = "ollama"
    GROQ = "groq" 
    GEMINI = "gemini"
    OPENROUTER = "openrouter"


class LLMFactory(ABC):
    """Abstract Factory for creating LLM models"""
    
    @abstractmethod
    def create_model(self, config: BaseModelConfig) -> LLMModel:
        """Create and return an LLM model instance"""
        pass


class OllamaFactory(LLMFactory):
    """Factory for creating Ollama models"""
    
    def create_model(self, config: OllamaConfig) -> OllamaModel:
        return OllamaModel(config)


class GroqFactory(LLMFactory):
    """Factory for creating Groq models"""
    
    def create_model(self, config: GroqConfig) -> GroqModel:
        return GroqModel(config)


class GeminiFactory(LLMFactory):
    """Factory for creating Gemini models"""
    
    def create_model(self, config: GeminiConfig) -> GeminiModel:
        return GeminiModel(config)


class OpenRouterFactory(LLMFactory):
    """Factory for creating OpenRouter models"""
    
    def create_model(self, config: OpenRouterConfig) -> OpenRouterModel:
        return OpenRouterModel(config)


class LLMFactoryRegistry:
    """Registry pattern to manage and create factories"""
    
    _factories: Dict[ModelType, Type[LLMFactory]] = {
        ModelType.OLLAMA: OllamaFactory,
        ModelType.GROQ: GroqFactory,
        ModelType.GEMINI: GeminiFactory,
        ModelType.OPENROUTER: OpenRouterFactory,
    }
    
    @classmethod
    def register_factory(cls, model_type: ModelType, factory_class: Type[LLMFactory]):
        """Register a new factory for a model type"""
        cls._factories[model_type] = factory_class
    
    @classmethod
    def get_factory(cls, model_type: ModelType) -> LLMFactory:
        """Get factory instance for the given model type"""
        factory_class = cls._factories.get(model_type)
        if not factory_class:
            raise ValueError(f"No factory registered for model type: {model_type.value}")
        return factory_class()
    
    @classmethod
    def create_model(cls, model_type: ModelType, config: BaseModelConfig) -> LLMModel:
        """Create a model using configuration object"""
        factory = cls.get_factory(model_type)
        return factory.create_model(config)
    
    @classmethod
    def create_model_with_params(cls, model_type: ModelType, model_name: str, **kwargs) -> LLMModel:
        """Create a model with individual parameters (creates config internally)"""
        config = ConfigManager.create_config(model_type.value, model_name=model_name, **kwargs)
        return cls.create_model(model_type, config)
    
    @classmethod
    def create_model_from_env(cls, model_type: ModelType, model_name: str) -> LLMModel:
        """Create a model using environment variables for configuration"""
        config = EnvironmentConfigLoader.load_config(model_type.value, model_name)
        return cls.create_model(model_type, config)
    
    @classmethod
    def get_supported_types(cls) -> list[str]:
        """Get list of supported model types"""
        return [model_type.value for model_type in cls._factories.keys()]


# Enhanced convenience factory class
class ModelFactory:
    """Enhanced factory class with multiple configuration options"""
    
    @staticmethod
    def create_model(model_type: str, model_name: str, **kwargs) -> LLMModel:
        """
        Create a model instance with individual parameters
        
        Args:
            model_type: Type of model ('ollama', 'groq', 'gemini', 'openrouter')
            model_name: Name of the specific model
            **kwargs: Model-specific configuration parameters
            
        Returns:
            LLMModel instance
        """
        try:
            model_type_enum = ModelType(model_type.lower())
            return LLMFactoryRegistry.create_model_with_params(model_type_enum, model_name, **kwargs)
        except ValueError as e:
            if "No factory registered" in str(e):
                raise e
            supported_types = LLMFactoryRegistry.get_supported_types()
            raise ValueError(f"Unsupported model type: {model_type}. Supported types: {supported_types}")
    
    @staticmethod
    def create_model_with_config(config: BaseModelConfig) -> LLMModel:
        """
        Create a model instance using a configuration object
        
        Args:
            config: Configuration object (OllamaConfig, GroqConfig, etc.)
            
        Returns:
            LLMModel instance
        """
        # Determine model type from config class
        config_type_map = {
            OllamaConfig: ModelType.OLLAMA,
            GroqConfig: ModelType.GROQ,
            GeminiConfig: ModelType.GEMINI,
            OpenRouterConfig: ModelType.OPENROUTER,
        }
        
        model_type = config_type_map.get(type(config))
        if not model_type:
            raise ValueError(f"Unknown configuration type: {type(config)}")
        
        return LLMFactoryRegistry.create_model(model_type, config)
    
    @staticmethod
    def create_model_from_env(model_type: str, model_name: str) -> LLMModel:
        """
        Create a model instance using environment variables
        
        Args:
            model_type: Type of model ('ollama', 'groq', 'gemini', 'openrouter')
            model_name: Name of the specific model
            
        Returns:
            LLMModel instance
        """
        try:
            model_type_enum = ModelType(model_type.lower())
            return LLMFactoryRegistry.create_model_from_env(model_type_enum, model_name)
        except ValueError as e:
            if "No environment loader" in str(e) or "validation failed" in str(e):
                raise e
            supported_types = LLMFactoryRegistry.get_supported_types()
            raise ValueError(f"Unsupported model type: {model_type}. Supported types: {supported_types}")
    
    @staticmethod
    def create_model_from_dict(config_dict: Dict[str, Any]) -> LLMModel:
        """
        Create a model instance from a configuration dictionary
        
        Args:
            config_dict: Dictionary containing model configuration
                        Must include 'model_type' key
        
        Returns:
            LLMModel instance
        """
        config = ConfigManager.from_dict(config_dict)
        return ModelFactory.create_model_with_config(config)
    
    @staticmethod
    def create_model_from_json(file_path: str, config_name: str) -> LLMModel:
        """
        Create a model instance from a JSON configuration file
        
        Args:
            file_path: Path to JSON configuration file
            config_name: Name of the configuration in the file
        
        Returns:
            LLMModel instance
        """
        configs = ConfigManager.from_json_file(file_path)
        if config_name not in configs:
            raise ValueError(f"Configuration '{config_name}' not found in {file_path}")
        
        config = configs[config_name]
        return ModelFactory.create_model_with_config(config)
    
    @staticmethod
    def get_supported_types() -> list[str]:
        """Get list of supported model types"""
        return LLMFactoryRegistry.get_supported_types()





        
        
        
        