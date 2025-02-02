import re
from discord.ext import commands
from ..utils.time_parser import parse_time

class MessageService:
    def extract_message_id(self, message_link: str) -> int:
        """Extract message ID from Discord message link"""
        pattern = r"discord\.com/channels/\d+/\d+/(\d+)"
        match = re.search(pattern, message_link)
        return int(match.group(1)) if match else None

    async def get_channel_messages(self, channel, limit=100, after=None, before=None):
        """Fetch messages from a channel"""
        messages = []
        
        # Use oldest_first=True to get messages in chronological order
        async for message in channel.history(limit=limit, after=after, before=before, oldest_first=True):
            # Skip messages from bots and commands
            if not message.author.bot and not message.content.startswith('!'):
                messages.append(message.content)
        return messages

    async def get_messages_between(self, channel, start_id, end_id):
        """Get messages between two message IDs"""
        messages = []
        started_collecting = False
        
        # Use oldest_first=True to get messages in chronological order
        async for message in channel.history(limit=None, oldest_first=True):
            if message.id == start_id:
                started_collecting = True
            
            # Add message if it's not from a bot and not a command
            if started_collecting and not message.author.bot and not message.content.startswith('!'):
                messages.append(message.content)
                
            if message.id == end_id:
                break
                
        return messages  # Already in chronological order