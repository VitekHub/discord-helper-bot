from .base import BaseSummaryCommand
from ..utils.argument_parser import ArgumentParser

class FilterSummaryCommand(BaseSummaryCommand):
    async def execute(self, args, vital=False):
        """Execute filter summary command"""
        try:
            status_message = "Analyzuji zprávy a hledám důležité informace..." if vital else "Načítám zprávy a generuji shrnutí..."
            await self.send_status(status_message)
            
            # Parse arguments
            parser = ArgumentParser(args)
            filters = parser.parse()
            
            # Get messages with filters
            messages = await self.message_service.get_channel_messages(
                self.ctx.channel,
                limit=filters.limit,
                after=filters.after,
                before=filters.before
            )
            
            if filters.mentioned_user:
                messages = [msg for msg in messages if filters.mentioned_user in msg]

            if vital:
                await self.send_vital_info(messages)
            else:
                await self.send_summary(messages)
                
        except Exception as e:
            await self.send_status(f"Chyba při zpracování příkazu: {str(e)}")