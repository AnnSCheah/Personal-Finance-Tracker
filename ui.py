import time
import os
from transactions import add_transaction, view_transactions, delete_transaction

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_terminal()
    print("Welcome to the Budget App!")
    print("What would you like to do?")
    for choice, function in choices.items():
        print(f"{list(choices.keys()).index(choice) + 1}. {choice}")

    user_choice = input("Enter your choice: ")

    if user_choice.lower() == "exit":
        exit()

    if not user_choice.isdigit() or int(user_choice) > len(choices) or int(user_choice) < 1:
        print("Invalid choice. Please try again.")
        time.sleep(0.5)
        main()

    choices[list(choices.keys())[int(user_choice) - 1]]()

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

    input("Press Enter to continue...")
    main()

def delete_expense():
    clear_terminal()
    view_transactions()
    transaction_id = input("Enter the ID of the transaction to delete (type \"cancel\" to go back): ")

    if transaction_id == "cancel":
        main()

    # check if ID is a number
    if not transaction_id.isdigit():
        print("Invalid ID. Please try again.")
        time.sleep(1)
        delete_expense()

    # check if transaction exists
    if not any(transaction["id"] == int(transaction_id) for transaction in view_transactions()):
        print("Transaction not found. Please try again.")
        time.sleep(1)
        delete_expense()

    delete_transaction(transaction_id)
    print("Transaction deleted successfully!")

    time.sleep(1)
    main()

def view_expenses():
    clear_terminal()
    view_transactions()

    input("Press Enter to continue...")
    main()

choices = {
    "Add an expense": add_expense,
    "Delete an expense": delete_expense,
    "View expenses": view_expenses,
    "Exit": exit
}



main()