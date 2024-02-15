import requests
from scraper import Scraper
from db.db import DB

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


class Crawler:
    def __init__(self, url) -> None:
        self.target_url = url


    def save_to_file(self, html,  filename="../data/content.html"):
        with open(filename, 'w') as f:
            f.write(html)

    def get_html(self):
        """Retrieves the HTML content of a given URL, handling errors appropriately."""

        # set user-agent
        user_agent = "A scrapper for learning"
        headers = {"User-Agent": user_agent}

        # perform GET request
        try:
            response = requests.get(self.target_url, headers=headers)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            logger.debug(F'Response: {response.text}')

            response.encoding = "utf-8"
            logger.info('HTML retrieved!')
            return response.text

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve HTML from {self.target_url}: {e}")
            raise  # re-raise the exception to be handled by the caller




if __name__=="__main__":
    target_url = 'https://www.scrapethissite.com/pages/simple/'
    crawler = Crawler(target_url)
    html = crawler.get_html()
    crawler.save_to_file(html=html)

    scraper = Scraper(html)
    # scraper.get_bulgaria_area()
    countries_data = scraper.get_countries_data()
    print(countries_data)

    db = DB()
    db.insert_countries_data(countries_data)





