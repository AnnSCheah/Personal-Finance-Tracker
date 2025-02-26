import os
import json

DATA_FILE = 'data.json'

# load all transactions from file
def load_transactions():
    if not os.path.exists(DATA_FILE):
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
        "id": len(transactions) + 1,
        "date": date,
        "amount": amount,
        "category": category,
        "remarks": remarks
    }
    transactions.append(new_transaction)
    save_transactions(transactions)