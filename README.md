# Discord Channel Summarizer Bot

A Discord bot that uses Google's Generative AI to summarize channel conversations.

## Features

- Summarize channel messages using Google's Gemini AI
- Configurable message limit
- Easy to use commands

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
   python bot-summarizer.py
   ```

## Commands

- `!summarize [number]` - Summarize the last [number] messages (default: 100)
- `!help_summary` - Show help information

## Example

```
User: !summarize 50
Bot: *Generates a summary of the last 50 messages in the channel*
```

## Notes

- The bot uses Google's Gemini Pro model for text generation
- The bot requires the Message Content Intent to be enabled in the Discord Developer Portal