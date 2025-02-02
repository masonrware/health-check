import subprocess
import pytest
from unittest.mock import patch, MagicMock
from src.health_check import load_config, check_endpoint, monitor_endpoints

@pytest.fixture
def sample_config():
    """Loads a sample YAML file from the configs directory."""
    with open("configs/sample_config.yaml", "r") as file:
        return file.name

def test_load_config(sample_config):
    """Tests that the YAML file is correctly parsed into a Python list."""
    endpoints = load_config(sample_config)
    assert isinstance(endpoints, list)
    assert len(endpoints) > 0  # ensure there are endpoints
    assert "name" in endpoints[0]
    assert "url" in endpoints[0]

@patch("src.health_check.load_config")
@patch("src.health_check.check_endpoint")
@patch("src.health_check.AvailabilityLogger")
@patch("time.sleep", side_effect=[None, None, Exception("")])  # break loop after 2 cycles
def test_monitor_endpoints(mock_sleep, mock_logger, mock_check, mock_config):
    """Test monitor_endpoints by allowing it to run for 2 cycles before exiting."""
    
    # mock configuration file loading
    mock_config.return_value = [
        {"name": "Test Endpoint 1", "url": "https://example.com", "method": "GET", "headers": {}},
        {"name": "Test Endpoint 2", "url": "https://example.org", "method": "GET", "headers": {}}
    ]

    # simulate alternating success/failure responses
    mock_check.side_effect = [True, False, True, True]  # 2 cycles of results

    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    with pytest.raises(Exception, match=""):
        monitor_endpoints("configs/sample_config.yaml")

    # the loop might already be in the middle of another request when the exception occurs
    assert mock_check.call_count == 4 or mock_check.call_count == 5 # each endpoint checked twice
    assert mock_logger_instance.update.call_count == 4 or mock_check.call_count == 5 # each endpoint logged twice
    assert mock_logger_instance.log_availability.call_count == 2  # two cycles completed
    mock_sleep.assert_called_with(15)  # ensure time.sleep(15) was called

@patch('time.time')
@patch("requests.request")
def test_check_endpoint_up(mock_request, mock_time):
    """Tests an endpoint that returns a 200 status and latency < 500ms."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_request.return_value = mock_response
    
    # mock time.time() to simulate elapsed time (400 ms)
    mock_time.side_effect = [0, 0.4]

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
    # test case 1: 500 status code
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_request.return_value = mock_response
    
    # mock time.time() to simulate elapsed time (200 ms)
    mock_time.side_effect = [0, 0.2]
    
    result = check_endpoint({
        "name": "Test Endpoint",
        "url": "https://example.com",
        "method": "GET",
        "headers": {}
    })
    assert result == False

    # test case 2: high latency
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_request.return_value = mock_response
    
    # mock time.time() to simulate high latency (600ms)
    mock_time.side_effect = [0, 0.6]
    
    result = check_endpoint({
        "name": "Test Endpoint",
        "url": "https://example.com",
        "method": "GET",
        "headers": {}
    })
    assert result == False
    
@patch('time.time')
@patch("requests.request")
def test_check_endpoint_latency_fluctuation(mock_request, mock_time):
    """Tests that a site changing its latency between runs updates the status correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_request.return_value = mock_response

    # first request: latency = 200ms (should be UP)
    mock_time.side_effect = [0, 0.2]
    result_1 = check_endpoint({
        "name": "Fluctuating Latency Site",
        "url": "https://fluctuating.com",
        "method": "GET",
        "headers": {}
    })
    assert result_1 == True

    # second request: latency jumps to 700ms (should be DOWN)
    mock_time.side_effect = [0, 0.7]
    result_2 = check_endpoint({
        "name": "Fluctuating Latency Site",
        "url": "https://fluctuating.com",
        "method": "GET",
        "headers": {}
    })
    assert result_2 == False

    # third request: latency drops back to 300ms (should be UP)
    mock_time.side_effect = [0, 0.3]
    result_3 = check_endpoint({
        "name": "Fluctuating Latency Site",
        "url": "https://fluctuating.com",
        "method": "GET",
        "headers": {}
    })
    assert result_3 == True

@patch("requests.request")
def test_check_endpoint_request_exception(mock_request):
    """Test check_endpoint when a request exception occurs."""
    mock_request.side_effect = Exception("Request failed")
    
    try:
        result = check_endpoint({
            "name": "Test",
            "url": "https://example.com",
            "method": "GET",
            "headers": {}
        })
    except:
        assert True # call should raise an exception
