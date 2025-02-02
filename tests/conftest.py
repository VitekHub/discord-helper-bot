"""
PyTest configuration and fixtures.
"""
import pytest
import discord
from unittest.mock import AsyncMock, MagicMock
from src.services.message_service import MessageService
from src.services.ai_service import AiService

@pytest.fixture
def mock_interaction():
    """Create a mock Discord interaction"""
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()
    interaction.followup = AsyncMock()
    interaction.channel = AsyncMock()
    return interaction

@pytest.fixture
def mock_message_service():
    """Create a mock message service"""
    service = AsyncMock(spec=MessageService)
    return service

@pytest.fixture
def mock_ai_service():
    """Create a mock AI service"""
    service = AsyncMock(spec=AiService)
    return service