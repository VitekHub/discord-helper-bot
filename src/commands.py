from discord.ext import commands
from .message_utils import get_channel_messages, get_messages_between, parse_time, extract_message_id
from .ai_service import get_ai_summary, get_vital_info
from datetime import datetime

class SummaryCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sum-links')
    async def sum_links(self, ctx, from_link: str, to_link: str):
        """Summarize messages between two message links"""
        try:
            # Extract message IDs
            start_id = extract_message_id(from_link)
            end_id = extract_message_id(to_link)
            
            if not start_id or not end_id:
                await ctx.send("Invalid message links. Please use valid Discord message links.")
                return
                
            await ctx.send("Fetching messages between the selected range...")
            
            # Get messages between IDs
            messages = await get_messages_between(ctx.channel, start_id, end_id)
            
            if not messages:
                await ctx.send("No messages found in the specified range.")
                return
                
            # Join messages and get summary
            conversation_text = "\n".join(messages)
            summary = await get_ai_summary(conversation_text)
            
            # Send summary
            await ctx.send(f"**Summary of {len(messages)} messages in selected range:**\n\n{summary}")
            
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name='sum', usage='[time/count] [user] [--after YYYY-MM-DD] [--before YYYY-MM-DD]')
    async def sum(self, ctx, *args):
        """Summarize messages with advanced filtering"""
        await ctx.send("Fetching messages and generating summary...")
        
        try:
            limit = 100
            after = None
            before = None
            mentioned_user = None

            # Parse arguments
            i = 0
            while i < len(args):
                arg = args[i]
                
                if arg.endswith(('h', 'd')):
                    after = parse_time(arg)
                    if after:
                        limit = None
                elif arg.isdigit():
                    limit = int(arg)
                elif arg.startswith('<@') and arg.endswith('>'):
                    mentioned_user = arg
                elif arg == '--after' and i + 1 < len(args):
                    try:
                        after = datetime.strptime(args[i + 1], '%Y-%m-%d')
                        i += 1
                    except ValueError:
                        await ctx.send("Invalid date format for --after. Use YYYY-MM-DD")
                        return
                elif arg == '--before' and i + 1 < len(args):
                    try:
                        before = datetime.strptime(args[i + 1], '%Y-%m-%d')
                        i += 1
                    except ValueError:
                        await ctx.send("Invalid date format for --before. Use YYYY-MM-DD")
                        return
                i += 1

            # Get messages with filters
            messages = await get_channel_messages(ctx.channel, limit, after, before)
            
            if mentioned_user:
                messages = [msg for msg in messages if mentioned_user in msg]

            if not messages:
                await ctx.send("No messages found to summarize.")
                return
                
            conversation_text = "\n".join(messages[::-1])
            summary = await get_ai_summary(conversation_text)
            
            await ctx.send(f"**Summary of last {len(messages)} messages:**\n\n{summary}")
            
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name='sum-ids')
    async def sum_ids(self, ctx, start_id: str, end_id: str):
        """Summarize messages between two message IDs"""
        try:
            try:
                start_id = int(start_id)
                end_id = int(end_id)
            except ValueError:
                await ctx.send("Invalid message IDs. Please use valid Discord message IDs.")
                return
                
            await ctx.send("Fetching messages between the selected IDs...")
            
            messages = await get_messages_between(ctx.channel, start_id, end_id)
            
            if not messages:
                await ctx.send("No messages found in the specified range.")
                return
                
            conversation_text = "\n".join(messages)
            summary = await get_ai_summary(conversation_text)
            
            await ctx.send(f"**Summary of {len(messages)} messages in selected range:**\n\n{summary}")
            
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name='vital')
    async def vital(self, ctx, *args):
        """Extract vital information from messages"""
        await ctx.send("Analyzuji zprávy a hledám důležité informace...")
        
        try:
            limit = 100
            after = None
            before = None
            mentioned_user = None

            # Parse arguments
            i = 0
            while i < len(args):
                arg = args[i]
                
                if arg.endswith(('h', 'd')):
                    after = parse_time(arg)
                    if after:
                        limit = None
                elif arg.isdigit():
                    limit = int(arg)
                elif arg.startswith('<@') and arg.endswith('>'):
                    mentioned_user = arg
                elif arg == '--after' and i + 1 < len(args):
                    try:
                        after = datetime.strptime(args[i + 1], '%Y-%m-%d')
                        i += 1
                    except ValueError:
                        await ctx.send("Neplatný formát data pro --after. Použijte YYYY-MM-DD")
                        return
                elif arg == '--before' and i + 1 < len(args):
                    try:
                        before = datetime.strptime(args[i + 1], '%Y-%m-%d')
                        i += 1
                    except ValueError:
                        await ctx.send("Neplatný formát data pro --before. Použijte YYYY-MM-DD")
                        return
                i += 1

            messages = await get_channel_messages(ctx.channel, limit, after, before)
            
            if mentioned_user:
                messages = [msg for msg in messages if mentioned_user in msg]

            if not messages:
                await ctx.send("Nenalezeny žádné zprávy k analýze.")
                return
                
            conversation_text = "\n".join(messages[::-1])
            vital_info = await get_vital_info(conversation_text)
            
            await ctx.send(f"**Důležité informace z {len(messages)} zpráv:**\n\n{vital_info}")
            
        except Exception as e:
            await ctx.send(f"Došlo k chybě: {str(e)}")

    @commands.command(name='sumhelp')
    async def sumhelp(self, ctx):
        """Show help information"""
        help_text = """
**Summary Bot - Advanced Usage:**

**Basic Commands:**
• `!sum [number]` - Summarize the last [number] messages (default: 100)
• `!sum-help` - Show this help message
• `!sum-links [first_message_link] [last_message_link]` - Summarize messages between two message links
• `!sum-ids [first_message_id] [last_message_id]` - Summarize messages between two message IDs
• `!vital [options]` - Extract vital information and key points

**Advanced Options:**
1. Time-based summary:
• `!sum 24h` - Last 24 hours
• `!sum 7d` - Last 7 days

2. User-specific summary:
• `!sum @username` - Summarize messages mentioning specific user

3. Date range summary:
• `!sum --after 2024-02-01 --before 2024-02-28` - Summarize messages between dates

**Examples:**
• `!sum 50` - Last 50 messages
• `!sum 24h @username` - User mentions in last 24 hours
• `!sum 7d --after 2024-01-01` - Last 7 days of messages after Jan 1, 2024
• `!sum-links [message_link1] [message_link2]` - Messages between two links
• `!sum-ids 1234567890 1234567891` - Messages between two IDs
"""
        await ctx.send(help_text)