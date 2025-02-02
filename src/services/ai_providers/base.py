from abc import ABC, abstractmethod

class BaseAiProvider(ABC):
    """Base class for AI providers"""
    
    @abstractmethod
    async def generate_content(self, prompt: str) -> str:
        """Generate content from prompt"""
        pass