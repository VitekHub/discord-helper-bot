import discord
from discord.ext import commands
from .config import DISCORD_TOKEN
from .commands.commands import SummaryCommands

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Add our commands
    await bot.add_cog(SummaryCommands(bot))

def run_bot():
    """Run the Discord bot"""
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file")
        return
        
    # Run the bot
    bot.run(DISCORD_TOKEN)