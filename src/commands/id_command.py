from .base import BaseSummaryCommand
from ..config import EPHEMERAL_MESSAGES

class IdSummaryCommand(BaseSummaryCommand):
    async def execute(self, start_id: str, end_id: str):
        """Execute ID summary command"""
        try:
            # Send initial response
            await self.interaction.response.defer(thinking=True, ephemeral=EPHEMERAL_MESSAGES)
            
            try:
                start_id = int(start_id)
                end_id = int(end_id)
            except ValueError:
                await self.interaction.followup.send(
                    "Neplatná ID zpráv. Použijte prosím platná Discord ID zpráv.",
                    ephemeral=EPHEMERAL_MESSAGES
                )
                return
                
            messages = await self.message_service.get_messages_between(
                self.interaction.channel, start_id, end_id
            )
            
            await self.send_summary(messages, "Shrnutí zpráv ve vybraném rozsahu")
            
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