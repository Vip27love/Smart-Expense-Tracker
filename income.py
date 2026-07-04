from db import Database
from datetime import datetime

class Income:

    def __init__(self):
        self.db = Database()
        self.connection = self.db.connect()
        self.cursor = self.db.get_cursor(self.connection)

    def add_income(self, user_id):

        amount = float(input("Enter Income Amount : "))
        source = input("Enter Source : ").strip().title()
        description = input("Enter Description : ").strip()
        income_date = input("Enter Date (YYYY-MM-DD) : ").strip()

        try:
            datetime.strptime(income_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid Date Format! Please use YYYY-MM-DD")
            return
        query = """
        INSERT INTO income
        (user_id, amount, source, description, income_date)
        VALUES(%s, %s, %s, %s, %s)
        """

        values = (
            user_id,
            amount,
            source,
            description,
            income_date
        )

        self.cursor.execute(query, values)
        self.connection.commit()

        print("Income Added Successfully")

    def view_income(self, user_id):

        query = """
        SELECT id, amount, source, description, income_date
        FROM income
        WHERE user_id = %s
        """

        self.cursor.execute(query, (user_id,))

        incomes = self.cursor.fetchall()

        if not incomes:
            print("No Income Found")
            return

        print("\n========== Income List ==========\n")

        for income in incomes:

            print(f"""
Income ID    : {income[0]}
Amount       : ₹{income[1]}
Source       : {income[2]}
Description  : {income[3]}
Date         : {income[4]}
-----------------------------------
""")