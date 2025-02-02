# Discord Channel Summarizer Bot

A Discord bot that uses Google's Gemini Pro AI to summarize channel conversations and extract vital information. Built with a modular and maintainable architecture.

## Features

- Summarize channel messages using Google's Gemini Pro AI
- Configurable message limit
- Extract vital information from conversations (in Czech)
- Filter messages by time, date range, and user mentions
- Easy to use commands
- Modular code structure
- Clean separation of concerns

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a Discord bot and get your token:
   - Go to https://discord.com/developers/applications
   - Create a new application
   - Go to the Bot section
   - Create a bot and copy the token
   - Enable Message Content Intent in the Bot section

3. Get your Google AI API key:
   - Go to https://makersuite.google.com/app/apikey
   - Create a new API key

4. Configure the bot:
   - Add your Discord bot token to the `.env` file
   - Add your Google AI API key to the `.env` file

5. Run the bot:
   ```bash
   python main.py
   ```

## Project Structure

```
src/
├── commands/           # Command handlers
│   ├── base.py        # Base command class
│   ├── commands.py    # Command registration
│   ├── filter_command.py
│   ├── help_command.py
│   ├── id_command.py
│   └── link_command.py
├── services/          # Core services
│   ├── ai_service.py  # AI integration
│   └── message_service.py
└── utils/            # Utility functions
    ├── argument_parser.py
    └── time_parser.py
```

## Commands

Basic Commands:
- `!sum [number]` - Summarize the last [number] messages (default: 100)
- `!sum-help` - Show help information
- `!sum-links [first_message_link] [last_message_link]` - Summarize messages between two message links
- `!sum-ids [first_message_id] [last_message_id]` - Summarize messages between two message IDs
- `!vital [options]` - Extract vital information and key points (Czech)

Advanced Options:
1. Time-based summary:
   - `!sum 24h` - Summarize messages from last 24 hours
   - `!sum 7d` - Summarize messages from last 7 days

2. User-specific summary:
   - `!sum @username` - Summarize messages mentioning specific user

3. Date range summary:
   - `!sum --after 2024-02-01 --before 2024-02-28` - Summarize messages between dates

## Examples

```
# Basic usage
!sum 50                    # Last 50 messages

# Time-based summaries
!sum 24h                   # Last 24 hours
!sum 7d                    # Last 7 days

# User-specific summaries
!sum @username            # Messages mentioning user
!sum 24h @username       # User mentions in last 24 hours

# Date range summaries
!sum --after 2024-02-01 --before 2024-02-28    # Messages between dates
!sum 7d --after 2024-01-01                     # Last 7 days after Jan 1, 2024

# Message link range summary
!sum-links https://discord.com/.../message1_id https://discord.com/.../message2_id

# Message ID range summary
!sum-ids 1234567890 1234567891

# Vital information extraction
!vital 50                    # Last 50 messages
!vital 24h                   # Last 24 hours
!vital @username            # Messages mentioning user
!vital --after 2024-02-01   # Messages after specific date
```

## Notes

- The bot uses Google's Gemini Pro model for text generation
- Code follows object-oriented design principles
- Each component has a single responsibility
- Message Content Intent must be enabled in the Discord Developer Portal
- The vital information extraction feature provides output in Czech language