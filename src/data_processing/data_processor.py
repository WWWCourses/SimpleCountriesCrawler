""" Module: data_processing

    This module provides a DataProcessor class for processing data from a target URL.

    It includes functionality to scrape data from the target URL using a Crawler,
    extract relevant information using a Scraper,
    and insert the data into a database using a DB instance.

    Classes:
        DataProcessor: A class for processing data from a target URL.

    Attributes:
        logger: A logger instance for logging messages related to data processing operations.

    Example:
        To use the DataProcessor class:
        >>> processor = DataProcessor(target_url='https://example.com')
        >>> processor.run()
"""

import logging
from typing import List

from src.data_processing.crawler import Crawler
from src.data_processing.scraper import Scraper, ScraperError
from src.db.db import DB
from src.shared_types import CountryData
from src.utils.setup_logging import setup_logger

# Set up logger
logger = setup_logger('data_processor', logging.DEBUG)


class DataProcessor:
    def __init__(self, target_url: str) -> None:
        """ Initialize a DataProcessor instance.

            Parameters:
                target_url (str): The URL from which to scrape data.
        """
        self.target_url = target_url
        self.db = DB(config_file='src/config.ini', section='mysql')

    def scrape_data(self) -> List[CountryData]:
        """ Scrape data from the target URL and extract relevant information.

            List[Dict[str, Union[str, float]]]: A list of dictionaries containing the scraped data.
        """
        crawler = Crawler(self.target_url)

        html = crawler.get_html()

        scraper = Scraper(html)
        try:
            countries_data = scraper.get_countries_data()
        except ScraperError as e:
            logger.error('Error scraping data: %s', e)

        logger.debug(countries_data[:10])
        logger.info('Fetched %s countries data', len(countries_data))

        return countries_data

    def insert_data(self, data: List[CountryData]) -> None:
        """ Insert the provided data into the database.

            Parameters:
                data (list): A list of dictionaries containing the data to insert.
        """
        self.db.insert_countries_data(data)

    def run(self) -> None:
        """ Run the data processing pipeline.

            This method scrapes data from the target URL,
            extracts relevant information,
            and inserts it into the database.
        """
        data = self.scrape_data()
        self.insert_data(data)
