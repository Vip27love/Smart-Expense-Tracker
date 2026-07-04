from db import Database
from datetime import datetime

class Expense:

    def __init__(self):
        self.db = Database()
        self.connection = self.db.connect()
        self.cursor = self.db.get_cursor(self.connection)

    def add_expense(self, user_id):

        amount = float(input("Enter Amount : "))
        category = input("Enter Category : ").strip()
        description = input("Enter Description : ").strip()
        date = input("Enter Date (YYYY-MM-DD) : ").strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid Date Format! Please use YYYY-MM-DD")
            return

        query = """
        INSERT INTO expenses
        (user_id, amount, category, description, expense_date)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            user_id,
            amount,
            category,
            description,
            date
        )

        self.cursor.execute(query, values)
        self.connection.commit()

        print("Expense Added Successfully")

        # Budget Check
        self.check_budget(user_id)

    def check_budget(self, user_id):

        # Get Budget
        self.cursor.execute(
            """
            SELECT monthly_budget
            FROM budgets
            WHERE user_id=%s
            """,
            (user_id,)
        )

        budget = self.cursor.fetchone()

        if budget is None:
            print("Please set your budget first.")
            return

        budget = float(budget[0])

        # Get Total Expense
        self.cursor.execute(
            """
            SELECT COALESCE(SUM(amount),0)
            FROM expenses
            WHERE user_id=%s
            """,
            (user_id,)
        )

        total = float(self.cursor.fetchone()[0])

        print("\n========== Budget Report ==========")
        print(f"Budget    : ₹{budget}")
        print(f"Spent     : ₹{total}")

        if total > budget:
            print(f"⚠️ Budget Exceeded by ₹{total-budget}")
        else:
            print(f"Remaining : ₹{budget-total}")

    def view_expense(self, user_id):

        query = """
        SELECT id, amount, category, description, expense_date
        FROM expenses
        WHERE user_id=%s
        """

        self.cursor.execute(query, (user_id,))
        expenses = self.cursor.fetchall()

        if not expenses:
            print("No Expense Found")
            return

        for expense in expenses:

            print("------------------------------")
            print("Expense ID :", expense[0])
            print("Amount     :", expense[1])
            print("Category   :", expense[2])
            print("Description:", expense[3])
            print("Date       :", expense[4])
            print("------------------------------")

    def update_expense(self, user_id):

        expense_id = int(input("Enter Expense ID : "))

        self.cursor.execute(
            """
            SELECT id
            FROM expenses
            WHERE id=%s AND user_id=%s
            """,
            (expense_id, user_id)
        )

        if not self.cursor.fetchone():
            print("Expense Not Found")
            return

        amount = float(input("Enter New Amount : "))
        category = input("Enter New Category : ").strip().title()
        description = input("Enter New Description : ").strip()
        expense_date = input("Enter New Date (YYYY-MM-DD) : ").strip()

        try:
          datetime.strptime(expense_date, "%Y-%m-%d")
        except ValueError:
          print("Invalid Date Format! Please use YYYY-MM-DD")
          return

        self.cursor.execute(
            """
            UPDATE expenses
            SET amount=%s,
                category=%s,
                description=%s,
                expense_date=%s
            WHERE id=%s
            AND user_id=%s
            """,
            (
                amount,
                category,
                description,
                expense_date,
                expense_id,
                user_id
            )
        )

        self.connection.commit()

        print("Expense Updated Successfully")

    def delete_expense(self, user_id):

        expense_id = int(input("Enter Expense ID : "))

        self.cursor.execute(
            """
            SELECT id
            FROM expenses
            WHERE id=%s
            AND user_id=%s
            """,
            (expense_id, user_id)
        )

        if not self.cursor.fetchone():
            print("Expense Not Found")
            return

        confirm = input("Are you sure? (Y/N): ").upper()

        if confirm != "Y":
            print("Deletion Cancelled")
            return

        self.cursor.execute(
            """
            DELETE FROM expenses
            WHERE id=%s
            AND user_id=%s
            """,
            (expense_id, user_id)
        )

        self.connection.commit()

        print("Expense Deleted Successfully")