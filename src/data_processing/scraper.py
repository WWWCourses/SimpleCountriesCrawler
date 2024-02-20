"""Module: scraper"""

import logging
import bs4
from typing import List

from src.utils.setup_logging import setup_logger
from src.shared_types import CountryData

logger = setup_logger('scraper', logging.ERROR)


class ScraperError(Exception):
    """Custom exception for errors related to Scraper."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class Scraper:
    """Class for scraping data from HTML."""

    def __init__(self, html: str) -> None:
        """Initializes a new Scraper object.

            Args:
                html (str): The HTML content to scrape.
        """
        self.html = html
        self.soup = bs4.BeautifulSoup(self.html, "html.parser")

    def _extract_text(self, element: bs4.element.Tag, css_selector: str) -> str:
        """Extracts text from an HTML element based on a CSS selector.

            Args:
                element (bs4.element.Tag): The HTML element to search within.
                css_selector (str): The CSS selector to use for extraction.

            Returns:
                str: The extracted text.
        """
        target_element = element.select_one(css_selector)
        if target_element:
            return target_element.text.strip()
        else:
            raise ScraperError(f"Cannot find '{css_selector}' in element:\n{element}")

    def _extract_float(self, element: bs4.element.Tag, css_selector: str) -> float:
        """Extracts a float value from an HTML element based on a CSS selector.

            Args:
                element (bs4.element.Tag): The HTML element to search within.
                css_selector (str): The CSS selector to use for extraction.

            Returns:
                float: The extracted float value.
        """
        text = self._extract_text(element, css_selector)
        try:
            return float(text)
        except ValueError as err:
            raise ScraperError(f"Cannot extract float value from: {text}") from err

    def get_countries_data(self) -> List[CountryData]:
        """Scrape data for all countries from self.html."""
        bg_country_area_selector = '#countries > div > div:nth-child(11) > div:nth-child(1) > div > span.country-area'
        bg_area = self._extract_float(self.soup, bg_country_area_selector)
        countries_data = []

        country_divs = self.soup.select('#countries div.country')
        for country_div in country_divs:
            try:
                country_name = self._extract_text(country_div, 'h3')
                country_capital = self._extract_text(country_div, '.country-capital')
                country_population = self._extract_text(country_div, '.country-population')
                country_area = self._extract_float(country_div, '.country-area')
            except ScraperError as err:
                logger.error(err)

            if country_area > bg_area:
                country_data = {
                    'name': country_name,
                    'capital': country_capital,
                    'population': country_population,
                    'area': country_area,
                }
                countries_data.append(country_data)


        return countries_data
