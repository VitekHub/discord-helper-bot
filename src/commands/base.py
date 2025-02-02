from discord.ext import commands
from ..services.message_service import MessageService
from ..services.ai_service import AiService

class BaseSummaryCommand:
    def __init__(self, ctx, message_service: MessageService, ai_service: AiService):
        self.ctx = ctx
        self.message_service = message_service
        self.ai_service = ai_service

    async def send_status(self, message):
        """Send status message to channel"""
        await self.ctx.send(message)

    async def send_summary(self, messages, summary_type="Summary"):
        """Send summary of messages"""
        if not messages:
            await self.send_status("No messages found to summarize.")
            return False

        conversation_text = "\n".join(messages[::-1])  # Reverse for chronological order
        summary = await self.ai_service.get_ai_summary(conversation_text)
        
        await self.ctx.send(f"**{summary_type} of {len(messages)} messages:**\n\n{summary}")
        return True

    async def send_vital_info(self, messages):
        """Send vital information from messages"""
        if not messages:
            await self.send_status("Nenalezeny žádné zprávy k analýze.")
            return False

        conversation_text = "\n".join(messages[::-1])
        vital_info = await self.ai_service.get_vital_info(conversation_text)
        
        await self.ctx.send(f"**Důležité informace z {len(messages)} zpráv:**\n\n{vital_info}")
        return True