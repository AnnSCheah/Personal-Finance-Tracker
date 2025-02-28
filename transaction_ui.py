"""Module for handling transaction-related UI operations."""

import time
from transactions import add_transaction, update_transaction, delete_transaction, load_transactions, delete_all_transactions
from categories import EXPENSE_CATEGORIES, INCOME_CATEGORIES

class TransactionUI:
    def __init__(self, display_manager):
        self.display = display_manager

    def add_transaction_ui(self, transaction_type="expense"):
        """Handle UI for adding a transaction."""
        amount = f"{float(input(f'Enter the {transaction_type}: $')):.2f}"
        date = input("Enter the date (DD/MM/YYYY): ")
        category = self.get_category(transaction_type)
        remark = input("Enter a remark (optional): ")

        add_transaction(date, amount, category, remark, transaction_type=transaction_type)

        print("")
        print(f"{transaction_type.capitalize()} added successfully!")
        self.display.show_transaction_details(amount, date, category, remark)

        input("\nPress Enter to continue...")
        return "manage_transactions"

    def edit_transaction_ui(self, transaction_type="expense"):
        """Handle UI for editing a transaction."""
        transactions = load_transactions()
        transactions_exist = self.display.show_filtered_transactions(transactions, transaction_type)

        if not transactions_exist:
            input("\nPress Enter to continue...")
            return "manage_transactions"

        transaction_id = input(f"Enter the ID of the {transaction_type} to edit (type \"cancel\" to go back): ")

        if transaction_id == "cancel":
            return "manage_transactions"

        if not self._validate_transaction_id(transaction_id, transactions, transaction_type):
            return self.edit_transaction_ui(transaction_type)

        transaction = next(t for t in transactions
                         if t["id"] == int(transaction_id) and t.get("type", "expense") == transaction_type)

        self.display.clear()
        self.display.show_edit_menu(transaction, transaction_type)
        detail_choice = input("Which detail would you like to edit? (1-5): ")

        if detail_choice == "5":
            return "manage_transactions"

        if not detail_choice.isdigit() or int(detail_choice) < 1 or int(detail_choice) > 5:
            print("Invalid choice. Please try again.")
            time.sleep(1)
            return self.edit_transaction_ui(transaction_type)

        updated_values = self._get_updated_values(detail_choice, transaction)
        update_transaction(transaction_id, **updated_values)

        print(f"\n{transaction_type.capitalize()} updated successfully!")
        details = {
            'amount': updated_values['amount'],
            'date': updated_values['date'],
            'category': updated_values['category'],
            'remarks': updated_values['remarks']
        }
        self.display.show_transaction_details(**details)

        input("\nPress Enter to continue...")
        return "manage_transactions"

    def delete_transaction_ui(self, transaction_type="expense"):
        """Handle UI for deleting a transaction."""
        transactions = load_transactions()
        transactions_exist = self.display.show_filtered_transactions(transactions, transaction_type)

        if not transactions_exist:
            input("\nPress Enter to continue...")
            return "manage_transactions"

        transaction_id = input(f"Enter the ID of the {transaction_type} to delete (type \"cancel\" to go back): ")

        if transaction_id == "cancel":
            return "manage_transactions"

        if not self._validate_transaction_id(transaction_id, transactions, transaction_type):
            return self.delete_transaction_ui(transaction_type)

        transaction = next(t for t in transactions
                         if t["id"] == int(transaction_id) and t.get("type", "expense") == transaction_type)

        self.display.clear()
        print(f"You are about to delete this {transaction_type}:")
        details = {
            'amount': transaction['amount'],
            'date': transaction['date'],
            'category': transaction['category'],
            'remarks': transaction['remarks']
        }
        self.display.show_transaction_details(**details)

        if not self._confirm_deletion(transaction_type):
            return "manage_transactions"

        delete_transaction(transaction_id)
        print(f"\n{transaction_type.capitalize()} deleted successfully!")
        time.sleep(1)
        return "manage_transactions"

    def delete_all_transactions(self):
        """Handle UI for deleting all transactions."""
        confirm = input("Are you sure you want to delete all transactions? (yes/no): ").lower()
        if confirm not in ["yes", "y"]:
            print("")
            print("Deletion cancelled.")
            time.sleep(1)
            return "manage_transactions"

        print("")
        print("This will delete all transactions from the database, and it cannot be undone.")
        absolute_confirm = input("Are you ABSOLUTELY sure you want to delete all transactions? (yes/no): ").lower()

        if absolute_confirm not in ["yes", "y"]:
            print("")
            print("Deletion cancelled.")
            time.sleep(1)
            return "manage_transactions"

        print("")
        print("Deleting all transactions...")
        time.sleep(2)

        delete_all_transactions()
        print("")
        print("All transactions have been deleted.")
        time.sleep(1)

        return "manage_transactions"



    def _validate_transaction_id(self, transaction_id, transactions, transaction_type):
        """Validate transaction ID input."""
        if not transaction_id.isdigit():
            print("Invalid ID. Please try again.")
            time.sleep(1)
            return False

        transaction_exists = any(t["id"] == int(transaction_id) and
                               t.get("type", "expense") == transaction_type
                               for t in transactions)

        if not transaction_exists:
            print(f"{transaction_type.capitalize()} transaction not found. Please try again.")
            time.sleep(1)
            return False

        return True

    def _get_updated_values(self, detail_choice, transaction):
        """Get updated values for transaction editing."""
        values = {
            'amount': transaction['amount'],
            'date': transaction['date'],
            'category': transaction['category'],
            'remarks': transaction['remarks']
        }

        if detail_choice == "1":
            values['amount'] = f"{float(input('Enter new amount: $')):.2f}"
        elif detail_choice == "2":
            values['date'] = input("Enter new date (DD/MM/YYYY): ")
        elif detail_choice == "3":
            values['category'] = input("Enter new category: ")
        elif detail_choice == "4":
            values['remarks'] = input("Enter new remark: ")

        return values

    def _confirm_deletion(self, transaction_type):
        """Confirm transaction deletion."""
        confirm = input(f"\nAre you sure you want to delete this {transaction_type}? (yes/no): ").lower()
        if confirm not in ["yes", "y"]:
            print(f"\n{transaction_type.capitalize()} deletion cancelled.")
            time.sleep(1)
            return False
        return True

    def get_category(self, transaction_type):
        """Get category from predefined list."""
        categories = EXPENSE_CATEGORIES if transaction_type == "expense" else INCOME_CATEGORIES

        print(f"\nAvailable {transaction_type} categories:")
        for idx, category in enumerate(categories, 1):
            print(f"{idx}. {category}")

        while True:
            try:
                choice = int(input("\nSelect category number: "))
                if 1 <= choice <= len(categories):
                    return categories[choice - 1]
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")