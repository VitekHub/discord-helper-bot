from discord.ext import commands
from .link_command import LinkSummaryCommand
from .id_command import IdSummaryCommand
from .filter_command import FilterSummaryCommand
from .find_command import FindCommand
from .help_command import HelpCommand
from ..services.message_service import MessageService
from ..services.ai_service import AiService

class SummaryCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_service = MessageService()
        self.ai_service = AiService()

    @commands.command(name='sum-links')
    async def sum_links(self, ctx, from_link: str, to_link: str):
        """Summarize messages between two message links"""
        command = LinkSummaryCommand(ctx, self.message_service, self.ai_service)
        await command.execute(from_link, to_link)

    @commands.command(name='sum', usage='[time/count] [user] [--after YYYY-MM-DD] [--before YYYY-MM-DD]')
    async def sum(self, ctx, *args):
        """Summarize messages with advanced filtering"""
        command = FilterSummaryCommand(ctx, self.message_service, self.ai_service)
        await command.execute(args)

    @commands.command(name='sum-ids')
    async def sum_ids(self, ctx, start_id: str, end_id: str):
        """Summarize messages between two message IDs"""
        command = IdSummaryCommand(ctx, self.message_service, self.ai_service)
        await command.execute(start_id, end_id)

    @commands.command(name='vital')
    async def vital(self, ctx, *args):
        """Extract vital information from messages"""
        command = FilterSummaryCommand(ctx, self.message_service, self.ai_service)
        await command.execute(args, vital=True)

    @commands.command(name='find')
    async def find(self, ctx, *args):
        """Find specific information in messages using custom prompt"""
        command = FindCommand(ctx, self.message_service, self.ai_service)
        await command.execute(args)

    @commands.command(name='sum-help')
    async def sumhelp(self, ctx):
        """Show help information"""
        await HelpCommand.execute(ctx)