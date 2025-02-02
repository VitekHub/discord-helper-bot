from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class BaseAiProvider(ABC):
    """Base class for AI providers"""
    
    @abstractmethod
    async def generate_content(self, prompt: str) -> str:
        """Generate content from prompt
        
        Args:
            prompt (str): The prompt to send to the AI
        
        Returns:
            str: The generated response
        """
        # Log the prompt
        logging.info("\n=== AI Prompt ===\n%s\n===============", prompt)
        pass