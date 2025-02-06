# Discord Helper Bot

A powerful Discord bot that leverages Google's Gemini Pro AI or Ollama to enhance your server communication. It can summarize conversations, extract vital information, and improve message formatting. Built with a modular architecture using Discord's slash commands.

## Features

Core Features:
- 🤖 Dual AI Support: Choose between Google's Gemini Pro or Ollama
- 📝 Message Summarization: Get concise summaries of conversations
- 🔍 Information Extraction: Find key points and vital information
- ✨ Message Enhancement: Improve formatting and readability

Technical Features:
- ⚡ Slash Commands: Easy-to-use interface with parameter hints
- 🔧 Flexible Configuration: Customizable message limits and filters
- 📅 Advanced Filtering: Filter by time, date range, and users
- 🏗️ Modular Architecture: Clean code structure and separation of concerns

## Setup

1. Install Python:
   - Download and install Python 3.8 or higher from [python.org](https://python.org)
   - Verify installation by running:
     ```bash
     python --version
     # or
     python3 --version
     ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a Discord bot and get your token:
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

4. Configure AI provider:
   
   Option A) Google AI (default):
   - Go to https://makersuite.google.com/app/apikey
   - Create a new API key
   - Set `AI_PROVIDER=google` in `.env`
   - Add your Google API key to `.env` as `GOOGLE_API_KEY`
   
   Option B) Ollama:
   - Install and run Ollama locally
   - Set `AI_PROVIDER=ollama` in `.env`
   - Configure `OLLAMA_HOST` and `OLLAMA_MODEL` in `.env`
   - For a tutorial on using Ollama, check out [this video guide](https://odysee.com/@NaomiBrockwell:4/Local-LLM:d)

5. Configure the bot:
   - Copy `.env.example` to `.env`
   - Add your Discord bot token
   - Configure your chosen AI provider

6. Run the bot:
   ```bash
   python main.py
   ```

## Project Structure

The project follows a clean, modular architecture designed for maintainability and extensibility:

```
src/
├── commands/              # Command handlers
│   ├── base.py           # Base command class with shared functionality
│   ├── commands.py       # Command registration and routing
│   ├── filter_command.py # Message filtering and summarization
│   ├── help_command.py   # Help documentation
│   ├── id_command.py     # Message ID-based operations
│   ├── link_command.py   # Message link-based operations
│   ├── find_command.py   # Custom prompt analysis
│   └── enhance_command.py # Message formatting enhancement
├── services/             # Core services
│   ├── ai_service.py     # AI provider integration
│   ├── message_service.py # Discord message handling
│   └── ai_providers/     # AI provider implementations
│       ├── base.py       # Base AI provider interface
│       ├── factory.py    # Provider factory pattern
│       ├── google_provider.py  # Google AI implementation
│       └── ollama_provider.py  # Ollama implementation
└── utils/               # Utility functions
    ├── argument_parser.py # Command argument parsing
    └── time_parser.py    # Time format handling
```

### Key Components

- **Commands**: Each command is implemented as a separate class, inheriting from `BaseSummaryCommand`
- **Services**: Core functionality separated into services for better maintainability
- **AI Providers**: Modular AI integration supporting multiple providers
- **Utils**: Shared utility functions for parsing and data handling

### Design Principles

- **Modularity**: Each component has a single responsibility
- **Extensibility**: Easy to add new commands or AI providers
- **Clean Architecture**: Clear separation of concerns
- **DRY (Don't Repeat Yourself)**: Common functionality shared through base classes

## Commands

### Basic Commands

- `/sum [count] [time] [@user] [--after date] [--before date]` - Summarize messages with filters
- `/help` - Show help information
- `/sum-links [first_message_link] [last_message_link]` - Summarize messages between two message links
- `/sum-ids [first_message_id] [last_message_id]` - Summarize messages between two message IDs
- `/vital [options]` - Extract vital information and key points
- `/enhance [message]` - Enhance message formatting using AI
- `/find [prompt] [options]` - Analyze messages using a custom prompt
- `/enhance [message]` - Enhance message formatting using AI

Advanced Options:
1. Time-based summary:
   - `/sum time:24h` - Summarize messages from last 24 hours
   - `/sum time:7d` - Summarize messages from last 7 days

2. User-specific summary:
   - `/sum user:@username` - Summarize messages mentioning specific user

3. Date range summary:
   - `/sum after:2024-02-01 before:2024-02-28` - Summarize messages between dates

## Examples

```bash
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

# Message enhancement
/enhance message:"Meeting tomorrow at 2pm to discuss project status"   # Enhance message formatting
/enhance message:"New feature: Added user authentication"              # Format feature announcement
```

## Notes
