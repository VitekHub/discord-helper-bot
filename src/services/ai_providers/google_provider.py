import google.generativeai as genai
from .base import BaseAiProvider
from ...config import GOOGLE_API_KEY

class GoogleAiProvider(BaseAiProvider):
    """Google AI provider implementation"""
    
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_content(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Chyba při generování obsahu: {str(e)}"