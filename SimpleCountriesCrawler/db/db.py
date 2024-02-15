from re import L
import mysql.connector

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class DB:
    def __init__(self) -> None:
        # Establish a connection to the MySQL server
        self.db = mysql.connector.connect(
            host="localhost",
            user="test",
            password="test1234",
            database="test"
        )

    def create_countries_table(self):
        # Create a cursor object to interact with the database
        cursor = self.db.cursor()

        # SQL query to create a 'students' table
        create_table_query = """
        CREATE TABLE countries (
          id INT AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(50),
          capital VARCHAR(50),
          population VARCHAR(50),
          area VARCHAR(50)
        )
        """



        # Execute the query to create the table
        cursor.execute(create_table_query)

    def insert_countries_data(self, countries_data):
        # Create a cursor object to interact with the database
        cursor = self.db.cursor()

        # SQL query to insert data into the 'students' table
        insert_query = """
            INSERT INTO countries (name, capital, population, area)
            VALUES (%s, %s, %s, %s)
        """

        # convert list of dictionaries into list of tupples, as executemany dit not works with list of dicstionaries
        countries_data = [
            (country['name'], country['capital'],country['population'],country['area'] )
            for country in countries_data
        ]

        cursor.executemany(insert_query, countries_data)

        # commit the transaction:
        self.db.commit()

        cursor.close()

if __name__=="__main__":
    db = DB()
    # db.create_countries_table()
    data = [
        {
            'name':" country_name1",
            'capital':"country_capital1",
            'population':"country_population1",
            'area':"country_area1",
        },
        {
            'name':" country_name1",
            'capital':"country_capital1",
            'population':"country_population1",
            'area':"country_area1",
        }
    ]

    db.insert_countries_data(data)

    logger.debug(f'Successfully insrted: {data}')