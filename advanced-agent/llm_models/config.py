"""
Configuration system for LLM models

This module provides a flexible configuration system that can handle
different configuration requirements for different model types.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from os import getenv
import json
from pathlib import Path


@dataclass
class BaseModelConfig(ABC):
    """Base configuration class for all models"""
    model_name: str
    temperature: float = 0.0
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        if not self.model_name:
            errors.append("model_name is required")
        if not isinstance(self.temperature, (int, float)) or self.temperature < 0:
            errors.append("temperature must be a non-negative number")
        return errors


@dataclass
class OllamaConfig(BaseModelConfig):
    """Configuration for Ollama models"""
    base_url: str = "http://localhost:11434"
    
    def validate(self) -> List[str]:
        errors = super().validate()
        if not self.base_url:
            errors.append("base_url is required for Ollama")
        return errors


@dataclass
class GroqConfig(BaseModelConfig):
    """Configuration for Groq models"""
    api_key: Optional[str] = None
    base_url: str = "https://api.groq.com/v1"
    max_retries: int = 2
    
    def __post_init__(self):
        if not self.api_key:
            self.api_key = getenv("GROQ_API_KEY")
    
    def validate(self) -> List[str]:
        errors = super().validate()
        if not self.api_key:
            errors.append("api_key is required for Groq (set GROQ_API_KEY environment variable)")
        return errors


@dataclass
class GeminiConfig(BaseModelConfig):
    """Configuration for Gemini models"""
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    
    def __post_init__(self):
        if not self.api_key:
            self.api_key = getenv("GOOGLE_API_KEY")
    
    def validate(self) -> List[str]:
        errors = super().validate()
        if not self.api_key:
            errors.append("api_key is required for Gemini (set GOOGLE_API_KEY environment variable)")
        return errors


@dataclass
class OpenRouterConfig(BaseModelConfig):
    """Configuration for OpenRouter models"""
    api_key: Optional[str] = None
    base_url: str = "https://openrouter.ai/api/v1"
    app_url: Optional[str] = None
    app_title: str = "LLM Agent"
    headers: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.api_key:
            self.api_key = getenv("OPENROUTER_API_KEY")
        if not self.app_url:
            self.app_url = getenv("APP_URL", "")
        if not self.app_title:
            self.app_title = getenv("APP_TITLE", "LLM Agent")
            
        # Set up default headers
        self.headers.update({
            "HTTP-Referer": self.app_url,
            "X-Title": self.app_title,
        })
    
    def validate(self) -> List[str]:
        errors = super().validate()
        if not self.api_key:
            errors.append("api_key is required for OpenRouter (set OPENROUTER_API_KEY environment variable)")
        return errors


class ConfigManager:
    """Manages configurations for different model types"""
    
    _config_classes = {
        "ollama": OllamaConfig,
        "groq": GroqConfig,
        "gemini": GeminiConfig,
        "openrouter": OpenRouterConfig,
    }
    
    @classmethod
    def create_config(cls, model_type: str, **kwargs) -> BaseModelConfig:
        """
        Create configuration for a specific model type
        
        Args:
            model_type: Type of model ('ollama', 'groq', 'gemini', 'openrouter')
            **kwargs: Configuration parameters
            
        Returns:
            Configuration instance
            
        Raises:
            ValueError: If model_type is not supported or configuration is invalid
        """
        config_class = cls._config_classes.get(model_type.lower())
        if not config_class:
            supported_types = list(cls._config_classes.keys())
            raise ValueError(f"Unsupported model type: {model_type}. Supported types: {supported_types}")
        
        config = config_class(**kwargs)
        errors = config.validate()
        if errors:
            error_msg = f"Configuration validation failed for {model_type}:\n" + "\n".join(f"  - {error}" for error in errors)
            raise ValueError(error_msg)
        
        return config
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> BaseModelConfig:
        """Create configuration from dictionary"""
        if "model_type" not in config_dict:
            raise ValueError("model_type is required in configuration dictionary")
        
        model_type = config_dict.pop("model_type")
        return cls.create_config(model_type, **config_dict)
    
    @classmethod
    def from_json_file(cls, file_path: str) -> Dict[str, BaseModelConfig]:
        """Load configurations from JSON file"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        configs = {}
        for name, config_data in data.items():
            configs[name] = cls.from_dict(config_data)
        
        return configs
    
    @classmethod
    def get_default_config(cls, model_type: str, model_name: str) -> BaseModelConfig:
        """Get default configuration for a model type"""
        return cls.create_config(model_type, model_name=model_name)
    
    @classmethod
    def get_supported_types(cls) -> List[str]:
        """Get list of supported model types"""
        return list(cls._config_classes.keys())


class EnvironmentConfigLoader:
    """Load configurations from environment variables"""
    
    @staticmethod
    def load_ollama_config(model_name: str) -> OllamaConfig:
        """Load Ollama configuration from environment"""
        return OllamaConfig(
            model_name=model_name,
            temperature=float(getenv("OLLAMA_TEMPERATURE", "0.0")),
            base_url=getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
    
    @staticmethod
    def load_groq_config(model_name: str) -> GroqConfig:
        """Load Groq configuration from environment"""
        return GroqConfig(
            model_name=model_name,
            temperature=float(getenv("GROQ_TEMPERATURE", "0.0")),
            api_key=getenv("GROQ_API_KEY"),
            base_url=getenv("GROQ_BASE_URL", "https://api.groq.com/v1"),
            max_retries=int(getenv("GROQ_MAX_RETRIES", "2"))
        )
    
    @staticmethod
    def load_gemini_config(model_name: str) -> GeminiConfig:
        """Load Gemini configuration from environment"""
        return GeminiConfig(
            model_name=model_name,
            temperature=float(getenv("GEMINI_TEMPERATURE", "0.0")),
            api_key=getenv("GOOGLE_API_KEY"),
            base_url=getenv("GEMINI_BASE_URL")
        )
    
    @staticmethod
    def load_openrouter_config(model_name: str) -> OpenRouterConfig:
        """Load OpenRouter configuration from environment"""
        return OpenRouterConfig(
            model_name=model_name,
            temperature=float(getenv("OPENROUTER_TEMPERATURE", "0.0")),
            api_key=getenv("OPENROUTER_API_KEY"),
            base_url=getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            app_url=getenv("APP_URL"),
            app_title=getenv("APP_TITLE", "LLM Agent")
        )
    
    _loaders = {
        "ollama": load_ollama_config,
        "groq": load_groq_config,
        "gemini": load_gemini_config,
        "openrouter": load_openrouter_config,
    }
    
    @classmethod
    def load_config(cls, model_type: str, model_name: str) -> BaseModelConfig:
        """Load configuration for a model type from environment variables"""
        loader = cls._loaders.get(model_type.lower())
        if not loader:
            raise ValueError(f"No environment loader for model type: {model_type}")
        
        config = loader(model_name)
        errors = config.validate()
        if errors:
            error_msg = f"Environment configuration validation failed for {model_type}:\n" + "\n".join(f"  - {error}" for error in errors)
            raise ValueError(error_msg)
        
        return config 