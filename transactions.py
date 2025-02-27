import os
import json

DATA_FILE = 'data.json'

# load all transactions from file
def load_transactions():
    if not os.path.exists(DATA_FILE):
        print("File not found")
        return []

    if os.path.getsize(DATA_FILE) == 0:
        print("File is empty")
        return []

    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# save a transaction to file
def save_transactions(transactions):
    with open(DATA_FILE, 'w') as file:
        json.dump(transactions, file, indent=4)

# add new transaction
def add_transaction(date, amount, category, remarks):
    transactions = load_transactions()
    new_transaction = {
        "id": transactions[-1]["id"] + 1 if transactions else 1,
        "date": date,
        "amount": amount,
        "category": category,
        "remarks": remarks
    }
    transactions.append(new_transaction)
    save_transactions(transactions)

# delete transaction
def delete_transaction(transaction_id):
    transactions = load_transactions()
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transactions.pop(transactions.index(transaction))
            break
    save_transactions(transactions)

# view expenses
def view_transactions():
    transactions = load_transactions()
    for expense in transactions:
        print("ID: {}".format(expense["id"]))
        print("Amount: ${}".format(expense["amount"]))
        print("Date: {}".format(expense["date"]))
        print("Category: {}".format(expense["category"]))
        print("Remark: {}".format(expense["remarks"]))
        print("")

    return transactions

