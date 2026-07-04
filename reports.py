from db import Database
import pandas as pd
import numpy as np


class Report:

    def __init__(self):
        self.db = Database()
        self.connection = self.db.connect()
        self.cursor = self.db.get_cursor(self.connection)

    def monthly_report(self, user_id):

        query = """
        SELECT amount, category, expense_date
        FROM expenses
        WHERE user_id = %s
        """

        self.cursor.execute(query, (user_id,))
        data = self.cursor.fetchall()

        df = pd.DataFrame(
            data,
            columns=[
                "Amount",
                "Category",
                "Date"
            ]
        )

        if df.empty:
            print("No Expense Found!")
            return

        print("\n===== Monthly Report =====")
        print(df)

        print("\n----- Pandas Report -----")
        print("Total Expense   :", df["Amount"].sum())
        print("Average Expense :", df["Amount"].mean())
        print("Highest Expense :", df["Amount"].max())
        print("Lowest Expense  :", df["Amount"].min())

        print("\nCategory Wise Expense")
        print(df.groupby("Category")["Amount"].sum())

        expense = np.array(df["Amount"])

        print("\n----- NumPy Report -----")
        print("Median              :", np.median(expense))
        print("Standard Deviation  :", np.std(expense))
        print("Variance            :", np.var(expense))

    def financial_summary(self, user_id):

        # Total Income
        self.cursor.execute(
            """
            SELECT COALESCE(SUM(amount),0)
            FROM income
            WHERE user_id=%s
            """,
            (user_id,)
        )

        total_income = float(self.cursor.fetchone()[0])

        # Total Expense
        self.cursor.execute(
            """
            SELECT COALESCE(SUM(amount),0)
            FROM expenses
            WHERE user_id=%s
            """,
            (user_id,)
        )

        total_expense = float(self.cursor.fetchone()[0])

        # Budget
        self.cursor.execute(
            """
            SELECT monthly_budget
            FROM budgets
            WHERE user_id=%s
            """,
            (user_id,)
        )

        budget = self.cursor.fetchone()

        if budget:
            budget = float(budget[0])
        else:
            budget = 0

        # Savings
        savings = total_income - total_expense

        # Remaining Budget
        remaining_budget = budget - total_expense

        # Percentages
        if total_income > 0:
            expense_percentage = (total_expense / total_income) * 100
            saving_percentage = (savings / total_income) * 100
        else:
            expense_percentage = 0
            saving_percentage = 0

        print("\n========== FINANCIAL SUMMARY ==========\n")

        print(f"Total Income        : ₹{total_income}")
        print(f"Total Expense       : ₹{total_expense}")
        print(f"Total Savings       : ₹{savings}")
        print(f"Monthly Budget      : ₹{budget}")
        print(f"Remaining Budget    : ₹{remaining_budget}")

        print(f"Expense Percentage  : {expense_percentage:.2f}%")
        print(f"Savings Percentage  : {saving_percentage:.2f}%")

        if savings < 0:
            print("\n⚠️ Warning! Your expenses are greater than your income.")
        else:
            print("\n✅ Great! You are saving money.")