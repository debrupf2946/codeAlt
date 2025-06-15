from abc import ABC, abstractmethod
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from typing import Optional
from os import getenv

class LLMModel(ABC):
    @abstractmethod
    def get_model(self) -> str:
        pass
    
    
    

class OllamaModel(LLMModel):
    def __init__(self, config):
        """Initialize with OllamaConfig object"""
        self.config = config
        
    def get_model(self) -> ChatOllama:
        return ChatOllama(
            model=self.config.model_name,
            temperature=self.config.temperature,
            base_url=self.config.base_url
        )
        
        
class GroqModel(LLMModel):
    def __init__(self, config):
        """Initialize with GroqConfig object"""
        self.config = config
        
    def get_model(self) -> ChatGroq:
        return ChatGroq(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_retries=self.config.max_retries,
            groq_api_key=self.config.api_key,
        )
     
        
        
class GeminiModel(LLMModel):
    def __init__(self, config):
        """Initialize with GeminiConfig object"""
        self.config = config
        
    def get_model(self) -> ChatGoogleGenerativeAI:
        return ChatGoogleGenerativeAI(  
            model=self.config.model_name,
            temperature=self.config.temperature,
            google_api_key=self.config.api_key,
            base_url=self.config.base_url
        )
        
class OpenRouterModel(LLMModel):
    def __init__(self, config):
        """Initialize with OpenRouterConfig object"""
        self.config = config
        
    def get_model(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            openai_api_key=self.config.api_key,
            openai_api_base=self.config.base_url,
            model_kwargs={
                "headers": self.config.headers
            },
        )
    
        