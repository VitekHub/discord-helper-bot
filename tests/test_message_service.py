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

@pytest.mark.asyncio
async def test_get_channel_messages(mocker):
    """Test fetching messages from a channel"""
    service = MessageService()
    
    # Create mock messages
    mock_message1 = mocker.Mock()
    mock_message1.author.bot = False
    mock_message1.content = mocker.Mock()
    mock_message1.content.startswith.return_value = False
    mock_message1.content.__str__.return_value = "Test message 1"
    
    mock_message2 = mocker.Mock()
    mock_message2.author.bot = True
    mock_message2.content = mocker.Mock()
    mock_message2.content.startswith.return_value = False
    mock_message2.content.__str__.return_value = "Bot message"
    
    mock_message3 = mocker.Mock()
    mock_message3.author.bot = False
    mock_message3.content = mocker.Mock()
    mock_message3.content.startswith.return_value = True
    mock_message3.content.__str__.return_value = "!command"
    
    # Create mock channel
    mock_channel = mocker.AsyncMock()
    mock_channel.history.return_value.__aiter__.return_value = [
        mock_message1,
        mock_message2,
        mock_message3
    ]
    
    # Test message filtering
    messages = await service.get_channel_messages(mock_channel, limit=10)
    assert len(messages) == 1
    assert messages[0] == "Test message 1"
    
    # Verify channel.history was called with correct parameters
    mock_channel.history.assert_called_once_with(
        limit=10,
        after=None,
        before=None,
        oldest_first=True
    )