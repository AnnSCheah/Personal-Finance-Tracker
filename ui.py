import time
from transactions import add_transaction

def main():
    print("Welcome to the Budget App!")
    print("What would you like to do?")
    print("1. Add an expense")
    print("2. View expenses")
    print("3. Exit")
    user_choice = input("Enter your choice: ")
    if user_choice == "1":
        add_expense()
    elif user_choice == "2":
        # view_expenses()
        print("View expenses")
    elif user_choice == "3" or user_choice == "exit":
        exit()
    else:
        print("Invalid choice. Please try again.\n")
        time.sleep(0.5)
        main()

def add_expense():
    amount = f"{float(input("Enter the expense: $")):.2f}"
    date = input("Enter the date (DD/MM/YYYY): ")
    category = input("Enter the category: ")
    remark = input("Enter a remark (optional): ")

    add_transaction(date, amount, category, remark)

    print("")
    print("Expense added successfully!")
    print("Amount: ${}".format(amount))
    print("Date: {}".format(date))
    print("Category: {}".format(category))
    print("Remark: {}".format(remark))
    print("")

    time.sleep(0.5)
    main()


main()