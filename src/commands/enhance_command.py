from .base import BaseSummaryCommand
from ..config import EPHEMERAL_MESSAGES

class EnhanceCommand(BaseSummaryCommand):
    async def execute(self, message: str):
        """Execute enhance command"""
        try:
            # Send initial response
            await self.interaction.response.defer(thinking=True, ephemeral=EPHEMERAL_MESSAGES)
            
            # Create the prompt
            prompt = f"""Udělej z tohoto Discord zprávu s nadpisy pomocí ## a s emoji před každým nadpisem, s dalším formátováním pomocí **, odrážkami, a s dalšími emoji apod. Můžeš text i rozvést nebo upravit formulaci. Výstup by měl být včetně formátování jako 'raw' text, který mohu přímo zkopírovat. Zde je zpráva:
{message}"""

            # Get enhanced version from AI
            enhanced = await self.ai_service.provider.generate_content(prompt)
            
            # Send both versions
            await self.interaction.followup.send(
                "🔒 *Tato zpráva je viditelná pouze pro Tebe*\n\n"
                "📝 **Původní zpráva:**\n"
                f"```\n{message}\n```\n"
                "👀 **Náhled vylepšené verze:**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{enhanced}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "✨ **Vylepšená verze ke zkopírování:**\n"
                "*Pro odeslání zkopíruj text z následujícího bloku:*\n"
                f"```\n{enhanced}\n```\n"
                "💡 *Tip: Klikni na tlačítko kopírování v pravém horním rohu kódového bloku*",
                ephemeral=EPHEMERAL_MESSAGES
            )
            
        except Exception as e:
            if not self.interaction.response.is_done():
                await self.interaction.response.send_message(
                    f"Chyba při zpracování příkazu: {str(e)}",
                    ephemeral=EPHEMERAL_MESSAGES
                )
            else:
                await self.interaction.followup.send(
                    f"Chyba při zpracování příkazu: {str(e)}",
                    ephemeral=EPHEMERAL_MESSAGES
                )