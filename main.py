from auth import Auth
from expense import Expense
from reports import Report
from charts import Charts
from export import Export
from budget import Budget
from income import Income

auth = Auth()
expense = Expense()
report = Report()
chart = Charts()
export = Export()
budget = Budget()
income = Income()

while True:

    print("\n1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter Choice : ")

    if choice == "1":

        auth.register()

    elif choice == "2":

        user_id = auth.login()

        if user_id:

            while True:

                print("\n===== DASHBOARD =====")
                print("1. Set Budget")
                print("2. Add Income")
                print("3. View Income")
                print("4. Add Expense")
                print("5. View Expense")
                print("6. Update Expense")
                print("7. Delete Expense")
                print("8. Monthly Report")
                print("9. Financial Summary")
                print("10. Charts")
                print("11. Export CSV")
                print("12. Logout")

                option = input("Enter Choice : ")

                if option == "1":

                    budget.set_budget(user_id)

                elif option == "2":

                    income.add_income(user_id)

                elif option == "3":

                    income.view_income(user_id)

                elif option == "4":

                    expense.add_expense(user_id)

                elif option == "5":

                    expense.view_expense(user_id)

                elif option == "6":

                    expense.update_expense(user_id)

                elif option == "7":

                    expense.delete_expense(user_id)

                elif option == "8":

                    report.monthly_report(user_id)

                elif option == "9":

                    report.financial_summary(user_id)

                elif option == "10":

                    print("\n===== CHARTS =====")
                    print("1. Pie Chart")
                    print("2. Bar Chart")

                    ch = input("Enter Choice : ")

                    if ch == "1":

                        chart.expense_pie_chart(user_id)

                    elif ch == "2":

                        chart.expense_bar_chart(user_id)

                    else:

                        print("Invalid Choice")

                elif option == "11":

                    export.export_csv(user_id)

                elif option == "12":

                    print("Logged Out Successfully")
                    break

                else:

                    print("Invalid Choice")

        else:

            print("Invalid Email or Password")

    elif choice == "3":

        print("Thank You for using Smart Expense Tracker!")
        break

    else:

        print("Invalid Choice")