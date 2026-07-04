from db import Database
import pandas as pd
import matplotlib.pyplot as plt


class Charts:

    def __init__(self):
        self.db = Database()
        self.connection = self.db.connect()
        self.cursor = self.db.get_cursor(self.connection)

    def expense_pie_chart(self, user_id):

        query = """
        SELECT category, amount
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
            columns=["Category", "Amount"]
        )

        # Decimal -> Float
        df["Amount"] = pd.to_numeric(df["Amount"])

        category_expense = df.groupby("Category")["Amount"].sum()

        plt.figure(figsize=(6, 6))

        plt.pie(
            category_expense.values,
            labels=category_expense.index,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Category Wise Expense")
        plt.show()

    def expense_bar_chart(self, user_id):

        query = """
        SELECT category, amount
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
            columns=["Category", "Amount"]
        )

        # Decimal -> Float
        df["Amount"] = pd.to_numeric(df["Amount"])

        category_expense = df.groupby("Category")["Amount"].sum()

        plt.figure(figsize=(8, 5))

        plt.bar(
            category_expense.index,
            category_expense.values
        )

        plt.title("Category Wise Expense")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.show()