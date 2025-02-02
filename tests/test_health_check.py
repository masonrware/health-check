import pytest
from unittest.mock import patch, MagicMock
from src.health_check import load_config, check_endpoint

@pytest.fixture
def sample_config():
    """Loads a sample YAML file from the configs directory."""
    with open("configs/sample_config.yaml", "r") as file:
        return file.name  # Return the file path

def test_parse_yaml_config(sample_config):
    """Tests that the YAML file is correctly parsed into a Python list."""
    endpoints = load_config(sample_config)
    assert isinstance(endpoints, list)
    assert len(endpoints) > 0  # Ensure there are endpoints
    assert "name" in endpoints[0]
    assert "url" in endpoints[0]

@patch('time.time')
@patch("requests.request")
def test_check_endpoint_up(mock_request, mock_time):
    """Tests an endpoint that returns a 200 status and latency < 500ms."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_request.return_value = mock_response
    
    # Mock time.time() to simulate elapsed time (400 ms)
    mock_time.side_effect = [0, 0.4]  # Start time and end time

    result = check_endpoint({
        "name": "Test Endpoint",
        "url": "https://example.com",
        "method": "GET",
        "headers": {}
    })
    assert result == True

@patch('time.time')
@patch("requests.request")
def test_check_endpoint_down(mock_request, mock_time):
    """Tests an endpoint that returns a 500 status or high latency."""
    # Test case 1: 500 status code
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_request.return_value = mock_response
    
    # Mock time.time() to simulate elapsed time (200 ms)
    mock_time.side_effect = [0, 0.2]  # Start time and end time
    
    result = check_endpoint({
        "name": "Test Endpoint",
        "url": "https://example.com",
        "method": "GET",
        "headers": {}
    })
    assert result == False

    # Test case 2: High latency
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_request.return_value = mock_response
    
    # Mock time.time() to simulate high latency (600ms)
    mock_time.side_effect = [0, 0.6]  # Start time and end time
    
    result = check_endpoint({
        "name": "Test Endpoint",
        "url": "https://example.com",
        "method": "GET",
        "headers": {}
    })
    assert result == False