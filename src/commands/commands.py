from discord import app_commands
import discord
from .link_command import LinkSummaryCommand
from .id_command import IdSummaryCommand
from .filter_command import FilterSummaryCommand
from .find_command import FindCommand
from .enhance_command import EnhanceCommand
from .help_command import HelpCommand
from ..services.message_service import MessageService
from ..services.ai_service import AiService

async def setup_commands(tree: app_commands.CommandTree):
    message_service = MessageService()
    ai_service = AiService()

    @tree.command(
        name="sum",
        description="Summarize messages with advanced filtering"
    )
    @app_commands.describe(
        count="Number of messages to summarize (default: 100)",
        time="Time range (e.g., 24h, 7d)",
        user="User to filter messages by",
        after="Start date (YYYY-MM-DD)",
        before="End date (YYYY-MM-DD)"
    )
    async def sum(
        interaction: discord.Interaction,
        count: int = None,
        time: str = None,
        user: discord.User = None,
        after: str = None,
        before: str = None
    ):
        command = FilterSummaryCommand(interaction, message_service, ai_service)
        args = []
        if count:
            args.append(str(count))
        if time:
            args.append(time)
        if user:
            args.append(user.mention)
        if after:
            args.extend(["--after", after])
        if before:
            args.extend(["--before", before])
        await command.execute(args)

    @tree.command(
        name="sum-links",
        description="Summarize messages between two message links"
    )
    @app_commands.describe(
        from_link="First message link",
        to_link="Last message link"
    )
    async def sum_links(
        interaction: discord.Interaction,
        from_link: str,
        to_link: str
    ):
        command = LinkSummaryCommand(interaction, message_service, ai_service)
        await command.execute(from_link, to_link)

    @tree.command(
        name="sum-ids",
        description="Summarize messages between two message IDs"
    )
    @app_commands.describe(
        start_id="First message ID",
        end_id="Last message ID"
    )
    async def sum_ids(
        interaction: discord.Interaction,
        start_id: str,
        end_id: str
    ):
        command = IdSummaryCommand(interaction, message_service, ai_service)
        await command.execute(start_id, end_id)

    @tree.command(
        name="vital",
        description="Extract vital information from messages"
    )
    @app_commands.describe(
        count="Number of messages to analyze (default: 100)",
        time="Time range (e.g., 24h, 7d)",
        user="User to filter messages by",
        after="Start date (YYYY-MM-DD)",
        before="End date (YYYY-MM-DD)"
    )
    async def vital(
        interaction: discord.Interaction,
        count: int = None,
        time: str = None,
        user: discord.User = None,
        after: str = None,
        before: str = None
    ):
        command = FilterSummaryCommand(interaction, message_service, ai_service)
        args = []
        if count:
            args.append(str(count))
        if time:
            args.append(time)
        if user:
            args.append(user.mention)
        if after:
            args.extend(["--after", after])
        if before:
            args.extend(["--before", before])
        await command.execute(args, vital=True)

    @tree.command(
        name="find",
        description="Find specific information in messages using custom prompt"
    )
    @app_commands.describe(
        prompt="Custom prompt for analysis",
        count="Number of messages to analyze (default: 100)",
        time="Time range (e.g., 24h, 7d)",
        user="User to filter messages by",
        after="Start date (YYYY-MM-DD)",
        before="End date (YYYY-MM-DD)"
    )
    async def find(
        interaction: discord.Interaction,
        prompt: str,
        count: int = None,
        time: str = None,
        user: discord.User = None,
        after: str = None,
        before: str = None
    ):
        command = FindCommand(interaction, message_service, ai_service)
        args = []
        if count:
            args.append(str(count))
        if time:
            args.append(time)
        if user:
            args.append(user.mention)
        if after:
            args.extend(["--after", after])
        if before:
            args.extend(["--before", before])
        args.append(f'"{prompt}"')
        await command.execute(args)

    @tree.command(
        name="help",
        description="Show help information"
    )
    async def help(interaction: discord.Interaction):
        await HelpCommand.execute(interaction)

    @tree.command(
        name="enhance",
        description="Vylepší formátování zprávy pomocí AI"
    )
    @app_commands.describe(
        message="Zpráva k vylepšení"
    )
    async def enhance(
        interaction: discord.Interaction,
        message: str
    ):
        command = EnhanceCommand(interaction, message_service, ai_service)
        await command.execute(message)