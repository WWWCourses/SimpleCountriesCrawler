import re
import bs4


import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Scraper:
    def __init__(self, html) -> None:
        self.html = html
        self.soup = bs4.BeautifulSoup(self.html, "html.parser" )


    def get_bulgaria_area(self)->float:
        area_span = self.soup.select_one(
            '#countries > div > div:nth-child(11) > div:nth-child(1) > div > span.country-area'
        )

        if area_span:
            try:
                area = float(area_span.text)
            except Exception as e:
                print(f"Can not extract area as float from : {area_span}")
                logger.debug(e)

        logger.debug(f'Bugaria area :{area}')
        return area

    def get_country_name(self, country_div):
        country_name = ""
        h3 = country_div.find('h3')
        if h3:
            country_name = h3.text.strip()

        return country_name


    def get_country_capital(self, country_div):
        # get country capital:
        country_capital = ""

        country_capital_span = country_div.select_one('.country-capital')
        if country_capital_span:
            country_capital = country_capital_span.text.strip()
        else:
            logger.debug(f"can not find '.country_capital' in {country_div}")

        return country_capital

    def get_country_population(self ,country_div):
        # get country population:
        country_population = country_div.select_one('.country-population').text.strip() # type:ignore
        return country_population

    def get_country_area(self, country_div):
        # get country area:
        country_area = country_div.select_one('.country-area').text.strip() # type:ignore
        country_area = float(country_area)

        return country_area


    def get_countries_data(self):
        """ Scrape data for all countries from self.html
            Info for a country:
                country_data = {
                    'name': name,
                    'capital':capital,
                    'population':population,
                    'area':area,
                }

            Return:
                countries_data: list of dictionaries
        """
        bg_area = self.get_bulgaria_area()
        countries_data = []

        country_divs = self.soup.select('#countries div.country')
        logger.debug(f"country_divs:")
        for country_div in country_divs:
            logger.debug(f"{country_div}\n")

            country_name = self.get_country_name(country_div)
            country_capital = self.get_country_capital(country_div)
            country_population = self.get_country_population(country_div)
            country_area = self.get_country_area(country_div)

            logger.debug(
                f"""country_name: {country_name},
                country_capital: {country_capital},
                country_population:{country_population},
                country_area: {country_area}"""
            )

            if country_area > bg_area:
                country_data = {
                    'name': country_name,
                    'capital':country_capital,
                    'population':country_population,
                    'area':country_area,
                }
                countries_data.append(country_data)

        return countries_data



