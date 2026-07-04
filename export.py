from db import Database
import pandas as pd


class Export:

    def __init__(self):
        self.db = Database()
        self.connection = self.db.connect()
        self.cursor = self.db.get_cursor(self.connection)

    def export_csv(self, user_id):

        query = """
        SELECT amount, category, description, expense_date
        FROM expenses
        WHERE user_id = %s
        """

        self.cursor.execute(query, (user_id,))

        data = self.cursor.fetchall()

        if not data:
            print("No Expense Found!")
            return

        df = pd.DataFrame(
            data,
            columns=[
                "Amount",
                "Category",
                "Description",
                "Date"
            ]
        )

        df.to_csv("expenses.csv", index=False)

        print("CSV Exported Successfully")