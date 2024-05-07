# import any libraries you want
import requests
import logging
from abc import ABC


class AbstractScraper(ABC):
    
    def __init__(self, retailer, country):
        self.retailer = retailer
        self.country = country
        # implement logger
        self.logger = logging.getLogger(self.__class__.__name__)

    # implement methods for sending GET and POST requests
    # these methods should be able to handle sending requests to the url with headers, cookies, params & json (POST requests only)
    def send_get_request(self, url, **kwargs):
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"Error in GET request: {e}")
            return None

    def send_post_request(self, url , **kwargs):
        try:
            response = requests.post(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"Error in POST request: {e}")
            return None

    # feel free to add any other methods you think you might need or could be useful