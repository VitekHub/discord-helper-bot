from .base import BaseSummaryCommand

class IdSummaryCommand(BaseSummaryCommand):
    async def execute(self, start_id: str, end_id: str):
        """Execute ID summary command"""
        try:
            try:
                start_id = int(start_id)
                end_id = int(end_id)
            except ValueError:
                await self.send_status("Neplatná ID zpráv. Použijte prosím platná Discord ID zpráv.")
                return
                
            await self.send_status("Načítám zprávy mezi vybranými ID...")
            
            messages = await self.message_service.get_messages_between(
                self.ctx.channel, start_id, end_id
            )
            
            await self.send_summary(messages, "Shrnutí zpráv ve vybraném rozsahu")