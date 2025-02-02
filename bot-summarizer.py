import os
import discord
from discord.ext import commands
import google.generativeai as genai
from datetime import datetime, timedelta
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure Google AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def get_channel_messages(channel, limit=100, after=None, before=None):
    """Fetch messages from a channel"""
    messages = []
    async for message in channel.history(limit=limit, after=after, before=before):
        messages.append(message.content)
    return messages

def parse_time(time_str):
    """Parse time string into datetime"""
    try:
        if time_str.endswith('h'):
            hours = int(time_str[:-1])
            return datetime.utcnow() - timedelta(hours=hours)
        elif time_str.endswith('d'):
            days = int(time_str[:-1])
            return datetime.utcnow() - timedelta(days=days)
        return None
    except ValueError:
        return None

async def get_ai_summary(text):
    """Get summary from Google AI"""
    prompt = f"Please provide a concise summary of the following conversation:\n\n{text}"

    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

async def get_vital_info(text):
    """Extract vital information from messages"""
    prompt = f"""Prosím analyzuj následující konverzaci a najdi a extrahuj pouze důležité informace a klíčová sdělení. Odstraň zbytečné části konverzace a small talk. Pokud najdeš obzvláště důležité zprávy, zkopíruj je doslovně. Pokud je to relevantní, zdůrazni termíny, deadliny nebo úkoly.

Text konverzace:

{text}"""

    print("\nPrompt sent to AI in get_vital_info:")
    print("----------------------------------------")
    print(prompt)
    print("----------------------------------------\n")

    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Chyba při generování analýzy: {str(e)}"

def extract_message_id(message_link):
    """Extract message ID from Discord message link"""
    pattern = r"discord\.com/channels/\d+/\d+/(\d+)"
    match = re.search(pattern, message_link)
    return int(match.group(1)) if match else None

async def get_messages_between(channel, start_id, end_id):
    """Get messages between two message IDs"""
    messages = []
    async for message in channel.history(limit=None):
        if message.id == end_id:
            messages.append(message.content)
        elif message.id == start_id:
            messages.append(message.content)
            break
        elif messages:  # If we've started collecting (after end_id)
            messages.append(message.content)
    return messages[::-1]  # Reverse to get chronological order

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='sum-links')
async def sum_links(ctx, from_link: str, to_link: str):
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

@bot.command(name='sum', usage='[time/count] [user] [--after YYYY-MM-DD] [--before YYYY-MM-DD]')
async def sum(ctx, *args):
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
            
            # Check for time-based limit
            if arg.endswith(('h', 'd')):
                after = parse_time(arg)
                if after:
                    limit = None  # Don't limit when using time-based filtering
            # Check for numeric limit
            elif arg.isdigit():
                limit = int(arg)
            # Check for user mention
            elif arg.startswith('<@') and arg.endswith('>'):
                mentioned_user = arg
            # Check for date filters
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
        
        # Filter by mentioned user if specified
        if mentioned_user:
            messages = [msg for msg in messages if mentioned_user in msg]

        if not messages:
            await ctx.send("No messages found to summarize.")
            return
            
        # Join messages into a single text
        conversation_text = "\n".join(messages[::-1])  # Reverse to get chronological order
        
        # Get AI summary
        summary = await get_ai_summary(conversation_text)
        
        # Send summary
        await ctx.send(f"**Summary of last {len(messages)} messages:**\n\n{summary}")
        
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name='sum-ids')
async def sum_ids(ctx, start_id: str, end_id: str):
    """Summarize messages between two message IDs"""
    try:
        # Convert string IDs to integers
        try:
            start_id = int(start_id)
            end_id = int(end_id)
        except ValueError:
            await ctx.send("Invalid message IDs. Please use valid Discord message IDs.")
            return
            
        await ctx.send("Fetching messages between the selected IDs...")
        
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

@bot.command(name='vital')
async def vital(ctx, *args):
    """Extract vital information from messages"""
    await ctx.send("Analyzuji zprávy a hledám důležité informace...")
    
    try:
        limit = 100
        after = None
        before = None
        mentioned_user = None

        # Parse arguments (same as sum command)
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

        # Get messages with filters
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

@bot.command(name='sumhelp')
async def sumhelp(ctx):
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

# Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN or not GOOGLE_API_KEY:
        print("Error: DISCORD_TOKEN or GOOGLE_API_KEY not found in .env file")
    else:
        bot.run(DISCORD_TOKEN)