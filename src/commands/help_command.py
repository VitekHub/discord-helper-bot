from discord.ext import commands

class HelpCommand:
    @staticmethod
    async def execute(ctx):
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