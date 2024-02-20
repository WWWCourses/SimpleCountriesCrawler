""" module db.py"""

import logging
from typing import List, Optional

import mysql.connector

from src.utils.setup_logging import setup_logger
from src.utils.config_loader import load_config
from src.shared_types import CountryData

logger = setup_logger("db", logging.DEBUG)


class DB:
    """Connects to a MySQL database and provides methods for creating
        and populating a 'countries' table.
    """

    def __init__(self, config_file: str, section: str = "mysql") -> None:
        """ Initializes a connection to the MySQL database specified in the configuration file.

            Args:
                config_file (str):
                    Path to the configuration file containing database credentials.
                section (str, optional):
                    Name of the section in the config file holding MySQL settings.
                    Defaults to "mysql".
        """

        mysql_config = load_config(config_file, section=section)

        try:
            self.db = mysql.connector.connect(**mysql_config)
            logger.info("Successfully connected to MySQL database '%s'", mysql_config["database"])
        except mysql.connector.Error as e:
            error_msg = f"Failed to connect to MySQL database: {e}"
            logger.error(error_msg)
            raise ConnectionError(error_msg) from e
        # finally:
        #     logger.debug("MySQL config data: %s", mysql_config)

    def create_countries_table(self) -> None:
        """Creates a 'countries' table in the database if it doesn't already exist."""

        query = """
            CREATE TABLE IF NOT EXISTS countries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                capital VARCHAR(50),
                population VARCHAR(50),
                area VARCHAR(50),
                created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """

        with self.db.cursor() as cursor:
            try:
                cursor.execute(query)
                self.db.commit()
            except mysql.connector.Error as e:
                logger.error('Error executing [%s]: %s', query, e)


    def insert_countries_data(self, countries_data: List[CountryData]) -> None:
        """Inserts a list of country data into the 'countries' table.

            Args:
                countries_data (List[CountryData]):
                    A list of dictionaries where each dictionary represents a country
                    with keys 'name', 'capital', 'population', and 'area'.
        """

        query = """
            INSERT INTO countries (name, capital, population, area)
            VALUES (%s, %s, %s, %s)
        """

        countries_data_tupples = [
            (country["name"], country["capital"], country["population"], country["area"])
            for country in countries_data
        ]

        with self.db.cursor() as cursor:
            try:
                cursor.executemany(query, countries_data_tupples)
                self.db.commit()
                logger.info("Successfully inserted: %s rows.", len(countries_data))
            except mysql.connector.Error as e:
                logger.error('Error executing [%s]: %s', query, e)



    def select_all_data(self):
        """Select all data from the 'countries' table.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the selected data.
        """
        query = "SELECT * FROM countries;"

        with self.db.cursor() as cursor:
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Successfully retrieved all: %s rows.", cursor.rowcount)
                logger.debug("All rows: %s",result[:10])
                return result
            except mysql.connector.Error as e:
                logger.error('Error executing [%s]: %s', query, e)


    def get_column_names(self) -> List[str]:
        """Retrieve the column names of the 'countries' table.

            Returns:
                List[str]: A list of column names.
        """
        query = "SELECT * FROM countries LIMIT 1;"
        column_names = []

        with self.db.cursor() as cursor:
            try:
                cursor.execute(query)
                row = cursor.fetchone()

                if row and cursor.description:
                    # Use cursor.description to get column names
                    column_names = [desc[0] for desc in cursor.description]
                    logger.info('Column names: %s', column_names)
                else:
                    logger.warning('No rows returned by query')
            except mysql.connector.Error as e:
                logger.error('Error executing [%s]: %s', query, e)

        return column_names

    def get_last_updated_date(self) -> Optional[str]:
        """Retrieve the last updated date from the 'countries' table.

            Returns:
                Optional[str]: The last updated date as a string, or None if no data is available.
        """
        query = 'SELECT MAX(updated_at) AS max_date FROM countries;'

        with self.db.cursor(dictionary=True) as cursor:
            try:
                cursor.execute(query)
                result = cursor.fetchone()
                if result and 'max_date' in result:
                    return result['max_date']   # type: ignore
                else:
                    raise ValueError('No data in table')
            except mysql.connector.Error as e:
                logger.error('Error executing [%s]: %s', query, e)


if __name__ == "__main__":
    db = DB("src/config.ini", section='mysql')
    # db.create_countries_table()

    data: List[CountryData] = [
        {
            "name": "country_name1",
            "capital": "country_capital1",
            "population": "country_population1",
            "area": 23,
        },
        {
            "name": "country_name2",
            "capital": "country_capital2",
            "population": "country_population2",
            "area": 45,
        },
    ]

    db.insert_countries_data(data)
