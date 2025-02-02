"""
Tests for Discord commands.
"""
import pytest
from src.commands.filter_command import FilterSummaryCommand
from src.commands.link_command import LinkSummaryCommand
from src.commands.id_command import IdSummaryCommand
from src.commands.find_command import FindCommand

@pytest.mark.asyncio
async def test_filter_command(mock_interaction, mock_message_service, mock_ai_service):
    """Test filter summary command"""
    command = FilterSummaryCommand(mock_interaction, mock_message_service, mock_ai_service)
    
    # Setup mocks
    mock_message_service.get_channel_messages.return_value = ["Message 1", "Message 2"]
    mock_ai_service.get_ai_summary.return_value = "Test summary"
    
    # Test command execution
    await command.execute(["50", "24h"])
    
    # Verify interactions
    mock_interaction.response.defer.assert_called_once()
    mock_message_service.get_channel_messages.assert_called_once()
    mock_ai_service.get_ai_summary.assert_called_once()

@pytest.mark.asyncio
async def test_link_command(mock_interaction, mock_message_service, mock_ai_service):
    """Test link summary command"""
    command = LinkSummaryCommand(mock_interaction, mock_message_service, mock_ai_service)
    
    # Setup mocks
    mock_message_service.extract_message_id.return_value = 123
    mock_message_service.get_messages_between.return_value = ["Message 1", "Message 2"]
    mock_ai_service.get_ai_summary.return_value = "Test summary"
    
    # Test command execution
    await command.execute(
        "https://discord.com/channels/123/456/789",
        "https://discord.com/channels/123/456/790"
    )
    
    # Verify interactions
    mock_interaction.response.defer.assert_called_once()
    assert mock_message_service.extract_message_id.call_count == 2
    mock_message_service.get_messages_between.assert_called_once()
    mock_ai_service.get_ai_summary.assert_called_once()

@pytest.mark.asyncio
async def test_find_command(mock_interaction, mock_message_service, mock_ai_service):
    """Test find command"""
    command = FindCommand(mock_interaction, mock_message_service, mock_ai_service)
    
    # Setup mocks
    mock_message_service.get_channel_messages.return_value = ["Message 1", "Message 2"]
    mock_ai_service.process_custom_prompt.return_value = "Test analysis"
    
    # Test command execution with quoted prompt
    await command.execute(['50', '"Find something"'])
    
    # Verify interactions
    mock_interaction.response.defer.assert_called_once()
    mock_message_service.get_channel_messages.assert_called_once()
    mock_ai_service.process_custom_prompt.assert_called_once()