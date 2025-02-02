from .ai_providers.factory import AiProviderFactory

class AiService:
    def __init__(self):
        self.provider = AiProviderFactory.create_provider()

    async def get_ai_summary(self, text: str) -> str:
        """Get summary from Google AI"""
        prompt = f"""Prosím poskytni stručné shrnutí následující konverzace. Odpověz v češtině:

{text}"""

        try:
            return await self.provider.generate_content(prompt)
        except Exception as e:
            return f"Chyba při generování shrnutí: {str(e)}"

    async def get_vital_info(self, text: str) -> str:
        """Extract vital information from messages"""
        prompt = f"""Prosím analyzuj následující konverzaci a najdi a extrahuj pouze důležité informace a klíčová sdělení. Odstraň zbytečné části konverzace a small talk. Pokud najdeš obzvláště důležité zprávy, zkopíruj je doslovně. Pokud je to relevantní, zdůrazni termíny, deadliny nebo úkoly.

Text konverzace:

{text}"""

        try:
            return await self.provider.generate_content(prompt)
        except Exception as e:
            return f"Chyba při generování analýzy: {str(e)}"