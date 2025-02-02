"""
Tests for the MessageService class.
"""
import pytest
from src.services.message_service import MessageService

@pytest.mark.asyncio
async def test_extract_message_id():
    """Test extracting message ID from Discord message link"""
    service = MessageService()
    
    # Test valid Discord message link
    link = "https://discord.com/channels/123456789/987654321/111222333"
    assert service.extract_message_id(link) == 111222333
    
    # Test invalid link
    assert service.extract_message_id("invalid_link") is None