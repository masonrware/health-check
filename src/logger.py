from collections import defaultdict

class AvailabilityLogger:
    """
    A class to track and log availability percentages for HTTP domains.
    """

    def __init__(self):
        """
        Initializes an empty availability tracker for domains.
        """
        self.availability = defaultdict(lambda: {"up": 0, "total": 0})

    def get_availability(self):
        """
        Getter method for returning availability tracker.
        """
        return self.availability
    
    def update(self, url, is_up):
        """
        Updates the availability statistics for a domain.
        
        :param url: The full URL of the endpoint.
        :param is_up: Boolean indicating if the endpoint was UP.
        """
        domain = self.extract_domain(url)
        self.availability[domain]["total"] += 1
        if is_up:
            self.availability[domain]["up"] += 1

    def extract_domain(self, url):
        """
        Extracts the domain from a given URL.
        
        :param url: The full HTTP/HTTPS URL.
        :return: The extracted domain.
        """
        return url.split("//")[-1].split("/")[0]  # extracts domain from URL

    def log_availability(self):
        """
        Prints the availability percentage of each tracked domain.
        """
        for domain, stats in self.availability.items():
            up_count = stats["up"]
            total_count = stats["total"]
            percentage = round((up_count / total_count) * 100)  # rounded to nearest whole number
            print(f"{domain} has {percentage}% availability percentage")
