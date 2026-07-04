import mysql.connector
from config import DB_CONFIG


class Database:

    def connect(self):

        try:

            connection = mysql.connector.connect(
                **DB_CONFIG,
                consume_results=True
            )

            if connection.is_connected():
                print("Database Connected Successfully")

            return connection

        except mysql.connector.Error as err:

            print("Database Connection Error:", err)
            return None

    def get_cursor(self, connection):

        return connection.cursor(buffered=True)