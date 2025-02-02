import argparse
import yaml
import requests
import time
from src.logger import AvailabilityLogger

def load_config(file_path):
    """
    Load the YAML configuration file containing endpoint definitions.
    
    :param file_path: Path to the YAML file.
    :return: Parsed YAML data as a Python list of dictionaries.
    """
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def check_endpoint(endpoint):
    """
    Send an HTTP request to the specified endpoint and determine if it is UP or DOWN.

    :param endpoint: A dictionary containing endpoint details such as URL, method, headers, and body.
    :return: (boolean) True if the endpoint is UP, False otherwise.
    """
    method = endpoint.get("method", "GET").upper()  # default to GET if not provided
    url = endpoint["url"]
    headers = endpoint.get("headers", {})  # default to an empty dictionary if headers are missing
    body = endpoint.get("body", None)

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=5)
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        # determine if the endpoint is UP
        is_up = 200 <= response.status_code < 300 and latency < 500  # 2xx response and latency < 500ms
        return is_up
    except requests.RequestException:
        # catch any connection errors, timeouts, etc., and return False (DOWN)
        return False

def monitor_endpoints(config_file):
    """
    Continuously monitor endpoints and log domain-level availability percentages.

    :param config_file: Path to the YAML configuration file.
    """
    endpoints = load_config(config_file)
    logger = AvailabilityLogger()

    while True:
        for endpoint in endpoints:
            url = endpoint["url"]
            is_up = check_endpoint(endpoint)
            logger.update(url, is_up)
        # print availability percentages
        logger.log_availability() 
        print("-" * 50)
        time.sleep(15) # 15 seconds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor HTTP endpoint availability from a YAML file.")
    parser.add_argument("config_file", help="Path to the YAML configuration file.")
    args = parser.parse_args()

    try:
        monitor_endpoints(args.config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
