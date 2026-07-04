from db import Database


class Budget:

    def __init__(self):
        self.db = Database()
        self.connection = self.db.connect()
        self.cursor = self.db.get_cursor(self.connection)

    def set_budget(self, user_id):

        budget = float(input("Enter Monthly Budget : "))

        self.cursor.execute(
            "SELECT * FROM budgets WHERE user_id = %s",
            (user_id,)
        )

        data = self.cursor.fetchone()

        if data:

            query = """
            UPDATE budgets
            SET monthly_budget = %s
            WHERE user_id = %s
            """

            self.cursor.execute(query, (budget, user_id))

        else:

            query = """
            INSERT INTO budgets(user_id, monthly_budget)
            VALUES(%s, %s)
            """

            self.cursor.execute(query, (user_id, budget))

        self.connection.reconnect()

        print("Budget Saved Successfully")

    def check_budget(self, user_id):

      

        self.cursor.execute(
            "SELECT monthly_budget FROM budgets WHERE user_id=%s",
            (user_id,)
        )

        budget = self.cursor.fetchone()

        if budget is None:
            print("Please set your budget first.")
            return

        budget = float(budget[0])

        self.cursor.execute(
            "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE user_id=%s",
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