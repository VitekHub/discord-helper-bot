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
        async for message in channel.history(limit=limit, after=after, before=before):
            messages.append(message.content)
        return messages

    async def get_messages_between(self, channel, start_id, end_id):
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