from datetime import datetime, timedelta
import re

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

def extract_message_id(message_link):
    """Extract message ID from Discord message link"""
    pattern = r"discord\.com/channels/\d+/\d+/(\d+)"
    match = re.search(pattern, message_link)
    return int(match.group(1)) if match else None

async def get_channel_messages(channel, limit=100, after=None, before=None):
    """Fetch messages from a channel"""
    messages = []
    async for message in channel.history(limit=limit, after=after, before=before):
        messages.append(message.content)
    return messages

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