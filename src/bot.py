import discord
from discord import app_commands
from .config import DISCORD_TOKEN
from .commands.commands import setup_commands

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

class SummaryBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Set up commands
        await setup_commands(self.tree)
        # Sync commands with Discord
        await self.tree.sync()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

def run_bot():
    """Run the Discord bot"""
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file")
        return
        
    # Create and run the bot
    bot = SummaryBot()
    bot.run(DISCORD_TOKEN)