from .base import BaseSummaryCommand
from ..config import EPHEMERAL_MESSAGES

class LinkSummaryCommand(BaseSummaryCommand):
    async def execute(self, from_link: str, to_link: str):
        """Execute link summary command"""
        try:
            # Send initial response
            await self.interaction.response.defer(thinking=True, ephemeral=EPHEMERAL_MESSAGES)
            
            start_id = self.message_service.extract_message_id(from_link)
            end_id = self.message_service.extract_message_id(to_link)
            
            if not start_id or not end_id:
                await self.send_status("Neplatné odkazy na zprávy. Použijte prosím platné odkazy na Discord zprávy.")
                return
                
            await self.send_status("Načítám zprávy ve vybraném rozsahu...")
            
            messages = await self.message_service.get_messages_between(
                self.interaction.channel, start_id, end_id
            )
            
            await self.send_summary(messages, "Shrnutí zpráv ve vybraném rozsahu")
            
        except Exception as e:
            # If we haven't responded yet, send an error response
            if not self.interaction.response.is_done():
                await self.interaction.response.send_message(
                    f"Chyba při zpracování příkazu: {str(e)}",
                    ephemeral=EPHEMERAL_MESSAGES
                )
            else:
                # Otherwise send a followup
                await self.interaction.followup.send(
                    f"Chyba při zpracování příkazu: {str(e)}",
                    ephemeral=EPHEMERAL_MESSAGES
                )