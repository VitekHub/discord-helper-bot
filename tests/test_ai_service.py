"""
Tests for the AiService class.
"""
import pytest
from src.services.ai_service import AiService

@pytest.mark.asyncio
async def test_get_ai_summary(mocker):
    """Test getting AI summary"""
    # Mock AI provider
    mock_provider = mocker.AsyncMock()
    mock_provider.generate_content.return_value = "Test summary"
    
    # Create AI service with mock provider
    service = AiService()
    service.provider = mock_provider
    
    # Test summary generation
    result = await service.get_ai_summary("Test conversation")
    assert result == "Test summary"
    
    # Verify provider was called with correct prompt
    mock_provider.generate_content.assert_called_once()
    call_args = mock_provider.generate_content.call_args[0][0]
    assert "Test conversation" in call_args

@pytest.mark.asyncio
async def test_get_vital_info(mocker):
    """Test getting vital information"""
    mock_provider = mocker.AsyncMock()
    mock_provider.generate_content.return_value = "Test vital info"
    
    service = AiService()
    service.provider = mock_provider
    
    result = await service.get_vital_info("Test conversation")
    assert result == "Test vital info"
    
    mock_provider.generate_content.assert_called_once()
    call_args = mock_provider.generate_content.call_args[0][0]
    assert "Test conversation" in call_args

@pytest.mark.asyncio
async def test_process_custom_prompt(mocker):
    """Test processing custom prompt"""
    mock_provider = mocker.AsyncMock()
    mock_provider.generate_content.return_value = "Test response"
    
    service = AiService()
    service.provider = mock_provider
    
    result = await service.process_custom_prompt("Test conversation", "Custom prompt")
    assert result == "Test response"
    
    mock_provider.generate_content.assert_called_once()
    call_args = mock_provider.generate_content.call_args[0][0]
    assert "Test conversation" in call_args
    assert "Custom prompt" in call_args