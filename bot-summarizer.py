import os
import discord
from discord.ext import commands
import google.generativeai as genai
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

async def get_channel_messages(channel, limit=100):
    """Fetch messages from a channel"""
    messages = []
    async for message in channel.history(limit=limit):
        messages.append(message.content)
    return messages

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

@bot.command(name='summarize')
async def summarize(ctx, limit: int = 100):
    """Summarize messages in the channel"""
    await ctx.send("Fetching messages and generating summary...")

    try:
        # Get messages
        messages = await get_channel_messages(ctx.channel, limit)
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
**Summary Bot Commands:**
• `!summarize [number]` - Summarize the last [number] messages (default: 100)
• `!help_summary` - Show this help message

Example:
`!summarize 50` - Summarize the last 50 messages
"""
    await ctx.send(help_text)

# Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN or not GOOGLE_API_KEY:
        print("Error: DISCORD_TOKEN or GOOGLE_API_KEY not found in .env file")
    else:
        bot.run(DISCORD_TOKEN)