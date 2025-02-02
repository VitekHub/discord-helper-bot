from .base import BaseAiProvider
from .google_provider import GoogleAiProvider
from .ollama_provider import OllamaAiProvider
from ...config import AI_PROVIDER

class AiProviderFactory:
    """Factory for creating AI providers"""
    
    @staticmethod
    def create_provider() -> BaseAiProvider:
        """Create an AI provider based on configuration"""
        if AI_PROVIDER == "google":
            return GoogleAiProvider()
        elif AI_PROVIDER == "ollama":
            return OllamaAiProvider()
        else:
            raise ValueError(f"Nepodporovaný AI provider: {AI_PROVIDER}")