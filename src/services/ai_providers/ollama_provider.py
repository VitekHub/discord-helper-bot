import aiohttp
from .base import BaseAiProvider
from ...config import OLLAMA_HOST, OLLAMA_MODEL

class OllamaAiProvider(BaseAiProvider):
    """Ollama AI provider implementation"""
    
    def __init__(self):
        self.base_url = OLLAMA_HOST
        self.model = OLLAMA_MODEL
    
    async def generate_content(self, prompt: str) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "")
                    else:
                        return f"Chyba: HTTP {response.status}"
        except Exception as e:
            return f"Chyba při generování obsahu: {str(e)}"