import os
import json
from src.utils.settings import DATA_FILE

# load all transactions from file
def load_transactions():
    if not os.path.exists(DATA_FILE):
        print("File not found")
        return []

    if os.path.getsize(DATA_FILE) == 0:
        print("File is empty")
        return []

    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

# save a transaction to file
def save_transactions(transactions):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(transactions, file, indent=4)

# add new transaction
def add_transaction(date, amount, category, remarks, transaction_type="expense"):
    transactions = load_transactions()
    new_transaction = {
        "id": transactions[-1]["id"] + 1 if transactions else 1,
        "date": date,
        "amount": amount,
        "category": category,
        "remarks": remarks,
        "type": transaction_type
    }
    transactions.append(new_transaction)
    save_transactions(transactions)

# delete transaction
def delete_transaction(transaction_id):
    transactions = load_transactions()
    for transaction in transactions:
        if transaction["id"] == int(transaction_id):
            transactions.pop(transactions.index(transaction))
            break
    save_transactions(transactions)

def delete_all_transactions():
    transactions = []
    save_transactions(transactions)

# view transactions of specified type
def view_filtered_transactions(transaction_type="expense"):
    transactions = load_transactions()

    if not transactions:
        print(f"No {transaction_type} transactions found.")
        return []

    filtered_transactions = [t for t in transactions if t.get('type', 'expense') == transaction_type]
    for transaction in filtered_transactions:
        print(f"ID: {transaction['id']}")
        print(f"Amount: ${transaction['amount']}")
        print(f"Date: {transaction['date']}")
        print(f"Category: {transaction['category']}")
        print(f"Remark: {transaction['remarks']}")
        print("")

    return filtered_transactions

# wrapper function for backward compatibility
def view_transactions():
    return view_filtered_transactions("expense")

# update transaction
def update_transaction(transaction_id, amount, category, date, remarks):
    transactions = load_transactions()
    for transaction in transactions:
        if transaction["id"] == int(transaction_id):
            transaction["amount"] = amount
            transaction["date"] = date
            transaction["category"] = category
            transaction["remarks"] = remarks
            break
    save_transactions(transactions)

# get total for a transaction type
def get_total(transaction_type="expense"):
    transactions = load_transactions()
    total = sum(float(transaction["amount"]) for transaction in transactions
                if transaction.get("type", "expense") == transaction_type)
    return f"{total:.2f}"

# wrapper functions for backward compatibility
def get_total_expenses():
    return get_total("expense")

def get_total_income():
    return get_total("income")
