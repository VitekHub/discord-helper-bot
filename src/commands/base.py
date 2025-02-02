import discord
from ..services.message_service import MessageService
from ..services.ai_service import AiService

class BaseSummaryCommand:
    def __init__(self, interaction: discord.Interaction, message_service: MessageService, ai_service: AiService):
        self.interaction = interaction
        self.message_service = message_service
        self.ai_service = ai_service

    async def send_status(self, message):
        """Send status message"""
        await self.interaction.response.send_message(message, ephemeral=True)

    async def send_summary(self, messages, summary_type="Shrnutí"):
        """Send summary of messages"""
        if not messages:
            await self.send_status("Nenalezeny žádné zprávy k analýze.")
            return False

        conversation_text = "\n".join(messages)  # Messages are already in chronological order
        summary = await self.ai_service.get_ai_summary(conversation_text)
        
        # If we haven't sent an initial response yet, use response.send_message
        if not self.interaction.response.is_done():
            await self.interaction.response.send_message(
                f"**{summary_type} z {len(messages)} zpráv** (bez příkazů a zpráv botů):\n\n{summary}",
                ephemeral=True
            )
        else:
            # Otherwise, use followup.send
            await self.interaction.followup.send(
                f"**{summary_type} z {len(messages)} zpráv** (bez příkazů a zpráv botů):\n\n{summary}",
                ephemeral=True
            )
        return True

    async def send_vital_info(self, messages):
        """Send vital information from messages"""
        if not messages:
            await self.send_status("Nenalezeny žádné zprávy k analýze.")
            return False

        conversation_text = "\n".join(messages)
        vital_info = await self.ai_service.get_vital_info(conversation_text)
        
        # If we haven't sent an initial response yet, use response.send_message
        if not self.interaction.response.is_done():
            await self.interaction.response.send_message(
                f"**Důležité informace z {len(messages)} zpráv** (bez příkazů a zpráv botů):\n\n{vital_info}",
                ephemeral=True
            )
        else:
            # Otherwise, use followup.send
            await self.interaction.followup.send(
                f"**Důležité informace z {len(messages)} zpráv** (bez příkazů a zpráv botů):\n\n{vital_info}",
                ephemeral=True
            )
        return True