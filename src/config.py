import os
from dotenv import load_dotenv

load_dotenv()

# Basic configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# AI Provider configuration
AI_PROVIDER = os.getenv('AI_PROVIDER', 'google')

# Google AI configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Ollama configuration
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')

# Bot configuration
EPHEMERAL_MESSAGES = os.getenv('EPHEMERAL_MESSAGES', 'true').lower() == 'true'