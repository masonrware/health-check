from src.logger import AvailabilityLogger

def test_logger_initial_state():
    """Tests that the logger initializes correctly with an empty state."""
    logger = AvailabilityLogger()
    assert logger.availability == {}

def test_logger_updates_correctly():
    """Tests that the logger correctly tracks availability percentages."""
    logger = AvailabilityLogger()
    
    # simulating requests to two domains
    logger.update("fetch.com", True)
    logger.update("fetch.com", False)
    logger.update("fetch.com", True)
    
    logger.update("www.fetchrewards.com", True)
    logger.update("www.fetchrewards.com", False)

    # fetch.com: 2/3 UP = 67%
    # www.fetchrewards.com: 1/2 UP = 50%
    availability = logger.get_availability()
    
    up_count = availability["fetch.com"]["up"]
    total_count = availability["fetch.com"]["total"]
    assert round((up_count / total_count) * 100) == 67
    
    up_count = availability["www.fetchrewards.com"]["up"]
    total_count = availability["www.fetchrewards.com"]["total"]
    assert round((up_count / total_count) * 100) == 50
