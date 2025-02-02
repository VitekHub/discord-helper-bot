# Discord Channel Summarizer Bot

A Discord bot that uses Google's Gemini Pro AI or Ollama to summarize channel conversations and extract vital information. Built with a modular and maintainable architecture using Discord's slash commands.

## Features

- Summarize channel messages using Google's Gemini Pro AI
- Alternative AI provider support (Ollama)
- Configurable message limit
- Extract vital information from conversations (in Czech)
- Filter messages by time, date range, and user mentions
- Easy to use slash commands with parameter hints
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
   - Create a bot and copy its token
   - Enable Message Content Intent in the Bot section
   - Under OAuth2 > URL Generator, select:
     - `bot` scope
     - `applications.commands` scope (required for slash commands)
     - Required bot permissions
   - Use the generated URL to invite the bot to your server

3. Configure AI provider:
   
   Option A) Google AI (default):
   - Go to https://makersuite.google.com/app/apikey
   - Create a new API key
   - Set `AI_PROVIDER=google` in `.env`
   - Add your Google API key to `.env`
   
   Option B) Ollama:
   - Install and run Ollama locally
   - Set `AI_PROVIDER=ollama` in `.env`
   - Configure `OLLAMA_HOST` and `OLLAMA_MODEL` in `.env`

4. Configure the bot:
   - Copy `.env.example` to `.env`
   - Add your Discord bot token
   - Configure your chosen AI provider

5. Run tests (optional):
   ```bash
   # Run all tests
   python -m pytest
   
   # Run tests with coverage report
   python -m pytest --cov=src --cov-report=term-missing
   ```

6. Run the bot:
   ```bash
   python main.py
   ```

## Project Structure

```
tests/                # Test suite
├── conftest.py      # Test configuration and fixtures
├── test_ai_service.py
├── test_commands.py
└── test_message_service.py

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
- `/sum [count] [time] [@user] [--after date] [--before date]` - Summarize messages with filters
- `/help` - Show help information
- `/sum-links [first_message_link] [last_message_link]` - Summarize messages between two message links
- `/sum-ids [first_message_id] [last_message_id]` - Summarize messages between two message IDs
- `/vital [options]` - Extract vital information and key points (Czech)
- `/find [prompt] [options]` - Analyze messages using a custom prompt

Advanced Options:
1. Time-based summary:
   - `/sum time:24h` - Summarize messages from last 24 hours
   - `/sum time:7d` - Summarize messages from last 7 days

2. User-specific summary:
   - `/sum user:@username` - Summarize messages mentioning specific user

3. Date range summary:
   - `/sum after:2024-02-01 before:2024-02-28` - Summarize messages between dates

## Examples

```
# Basic usage
/sum count:50                    # Last 50 messages

# Time-based summaries
/sum time:24h                    # Last 24 hours
/sum time:7d                     # Last 7 days

# User-specific summaries
/sum user:@username             # Messages mentioning user
/sum time:24h user:@username    # User mentions in last 24 hours

# Date range summaries
/sum after:2024-02-01 before:2024-02-28    # Messages between dates
/sum time:7d after:2024-01-01              # Last 7 days after Jan 1, 2024

# Message link range summary
/sum-links from_link:https://discord.com/.../message1_id to_link:https://discord.com/.../message2_id

# Message ID range summary
/sum-ids start_id:1234567890 end_id:1234567891

# Vital information extraction
/vital count:50                     # Last 50 messages
/vital time:24h                     # Last 24 hours
/vital user:@username               # Messages mentioning user
/vital after:2024-02-01            # Messages after specific date

# Custom prompt analysis
/find prompt:"Find all meeting dates" count:100                    # Search in last 100 messages
/find prompt:"What technical decisions were made?" time:24h        # Analyze last 24 hours
/find prompt:"What is this person responsible for?" user:@username # Analyze user mentions
/find prompt:"What was discussed about the API?"                   # Default: last 100 messages
```

## Notes

- Supports both Google's Gemini Pro and Ollama for text generation
- Code follows object-oriented design principles
- Each component has a single responsibility
- Message Content Intent must be enabled in the Discord Developer Portal
- Bot requires `applications.commands` scope for slash commands
- The vital information extraction feature provides output in Czech language
- The find command allows custom analysis using any prompt

## Testing

The project includes a comprehensive test suite using pytest. Key test features:

- Unit tests for all major components
- Async test support via pytest-asyncio
- Mock objects for Discord interactions
- Coverage reporting

Run tests using:
```bash
# Run all tests
python -m pytest

# Run tests with coverage report
python -m pytest --cov=src --cov-report=term-missing
```

Test coverage helps identify untested code paths and ensures robust functionality.