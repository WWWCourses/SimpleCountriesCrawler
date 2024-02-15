import mysql.connector
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class DB:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
            host="localhost",
            user="test",
            password="test1234",
            database="test"
        )

    def create_countries_table(self):
        cursor = self.db.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS countries (
          id INT AUTO_INCREMENT PRIMARY KEY,
          name VARCHAR(50),
          capital VARCHAR(50),
          population VARCHAR(50),
          area VARCHAR(50)
        )
        """

        try:
            cursor.execute(create_table_query)
            self.db.commit()
        except mysql.connector.Error as err:
            logger.error(f"Error creating table: {err}")
        finally:
            cursor.close()

    def insert_countries_data(self, countries_data):
        cursor = self.db.cursor()

        insert_query = """
            INSERT INTO countries (name, capital, population, area)
            VALUES (%s, %s, %s, %s)
        """

        # convert list of dictionaries into list of tuples needed for executemany:
        countries_data = [
            (country['name'], country['capital'], country['population'], country['area'])
            for country in countries_data
        ]

        try:
            cursor.executemany(insert_query, countries_data)
            self.db.commit()
            logger.debug(f"Successfully inserted: {len(countries_data)} rows.")
        except mysql.connector.Error as err:
            logger.error(f"Error inserting data: {err}")
        finally:
            cursor.close()

if __name__ == "__main__":
    db = DB()
    # db.create_countries_table()

    data = [
        {
            'name': "country_name1",
            'capital': "country_capital1",
            'population': "country_population1",
            'area': "country_area1",
        },
        {
            'name': "country_name2",
            'capital': "country_capital2",
            'population': "country_population2",
            'area': "country_area2",
        }
    ]

    db.insert_countries_data(data)
