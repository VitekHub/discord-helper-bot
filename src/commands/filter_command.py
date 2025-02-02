from .base import BaseSummaryCommand
from ..utils.argument_parser import ArgumentParser
import discord

class FilterSummaryCommand(BaseSummaryCommand):
    async def execute(self, args, vital=False):
        """Execute filter summary command"""
        try:
            # Send initial response
            await self.interaction.response.defer(thinking=True, ephemeral=True)
            
            # Parse arguments
            parser = ArgumentParser(args)
            filters = parser.parse()
            
            # Get messages with filters
            messages = await self.message_service.get_channel_messages(
                self.interaction.channel,
                limit=filters.limit,
                after=filters.after,
                before=filters.before
            )
            
            if filters.mentioned_user:
                messages = [msg for msg in messages if filters.mentioned_user in msg]

            # Send the appropriate response
            if vital:
                await self.send_vital_info(messages)
            else:
                await self.send_summary(messages)
                
        except Exception as e:
            # If we haven't responded yet, send an error response
            if not self.interaction.response.is_done():
                await self.interaction.response.send_message(
                    f"Chyba při zpracování příkazu: {str(e)}",
                    ephemeral=True
                )
            else:
                # Otherwise send a followup
                await self.interaction.followup.send(
                    f"Chyba při zpracování příkazu: {str(e)}",
                    ephemeral=True
                )