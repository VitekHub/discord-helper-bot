from .base import BaseSummaryCommand

class IdSummaryCommand(BaseSummaryCommand):
    async def execute(self, start_id: str, end_id: str):
        """Execute ID summary command"""
        try:
            try:
                start_id = int(start_id)
                end_id = int(end_id)
            except ValueError:
                await self.send_status("Invalid message IDs. Please use valid Discord message IDs.")
                return
                
            await self.send_status("Fetching messages between the selected IDs...")
            
            messages = await self.message_service.get_messages_between(
                self.ctx.channel, start_id, end_id
            )
            
            await self.send_summary(messages, "Summary of messages in selected range")