import os
import discord
from discord.ext import commands
import google.generativeai as genai
from datetime import datetime, timedelta
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

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

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

@bot.command(name='help_summary')
async def help_summary(ctx):
    """Show help information"""
    help_text = """
**Summary Bot - Advanced Usage:**

**Basic Commands:**
• `!sum [number]` - Summarize the last [number] messages (default: 100)
• `!help_summary` - Show this help message

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
"""
    await ctx.send(help_text)

# Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN or not GOOGLE_API_KEY:
        print("Error: DISCORD_TOKEN or GOOGLE_API_KEY not found in .env file")
    else:
        bot.run(DISCORD_TOKEN)