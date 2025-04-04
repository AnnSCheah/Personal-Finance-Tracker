"""Module for handling transaction-related UI operations."""

import time
from src.utils.settings import IDLE_TIME
from src.ui.category_ui import CategoryUI
from src.models.transaction import add_transaction, update_transaction, delete_transaction, load_transactions, delete_all_transactions

class TransactionUI:
    def __init__(self, display_manager):
        self.display = display_manager
        self.categories = CategoryUI(display_manager)

    def add_transaction_ui(self, transaction_type="expense"):
        """Handle UI for adding a transaction."""
        print(f"Add {transaction_type.capitalize()}")
        print("----------------------")
        amount = self._validate_expense_amount()
        if amount is None:
            return "manage_transactions"

        date = input("Enter the date (DD/MM/YYYY): ") # TODO: Find a better way to validate date.
        category = self._get_categories(transaction_type)
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

        # Check if the transaction ID is valid
        if not self._validate_transaction_id(transaction_id, transactions, transaction_type):
            return self.edit_transaction_ui(transaction_type)

        # Get the transaction to edit
        transaction = next(t for t in transactions
                        if t["id"] == int(transaction_id) and t.get("type", "expense") == transaction_type)

        self.display.clear()
        self.display.show_edit_menu(transaction, transaction_type)
        detail_choice = input("Which detail would you like to edit? (1-5): ")

        # Check if the user wants to go back
        if detail_choice == "5":
            return "manage_transactions"

        # Input validation
        if not detail_choice.isdigit() or int(detail_choice) < 1 or int(detail_choice) > 5:
            print("Invalid choice. Please try again.")
            time.sleep(IDLE_TIME)
            return self.edit_transaction_ui(transaction_type)


        updated_values = self._get_updated_values(detail_choice, transaction)

        # Check if the user wants to cancel the operation
        if updated_values is None:
            self.display.clear()
            return self.edit_transaction_ui(transaction_type)

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
        time.sleep(IDLE_TIME)
        return "manage_transactions"

    def delete_all_transactions(self):
        """Handle UI for deleting all transactions."""
        confirm = input("Are you sure you want to delete all transactions? (yes/no): ").lower()
        if confirm not in ["yes", "y"]:
            print("")
            print("Deletion cancelled.")
            time.sleep(IDLE_TIME)
            return "manage_transactions"

        print("")
        print("This will delete all transactions from the database, and it cannot be undone.")
        absolute_confirm = input("Are you ABSOLUTELY sure you want to delete all transactions? (yes/no): ").lower()

        if absolute_confirm not in ["yes", "y"]:
            print("")
            print("Deletion cancelled.")
            time.sleep(IDLE_TIME)
            return "manage_transactions"

        print("")
        print("Deleting all transactions...")
        time.sleep(2)

        delete_all_transactions()
        print("")
        print("All transactions have been deleted.")
        time.sleep(IDLE_TIME)

        return "manage_transactions"

    def _validate_transaction_id(self, transaction_id, transactions, transaction_type):
        """Validate transaction ID input."""
        if not transaction_id.isdigit():
            print("Invalid ID. Please try again.")
            time.sleep(IDLE_TIME)
            self.display.clear()
            return False

        transaction_exists = any(t["id"] == int(transaction_id) and
                            t.get("type", "expense") == transaction_type
                            for t in transactions)

        if not transaction_exists:
            print(f"{transaction_type.capitalize()} transaction not found. Please try again.")
            time.sleep(IDLE_TIME)
            self.display.clear()
            return False

        return True

    def _validate_expense_amount(self):
        """Validate expense amount input."""
        amount = input('Enter the amount (or type \"cancel\" to go back): $')

        if amount.lower() == "cancel":
            return None

        # Remove any whitespace
        amount = amount.strip()

        # Check if amount if empty
        if not amount:
            print("Amount cannot be empty. Please try again.")
            time.sleep(IDLE_TIME)
            return self._validate_expense_amount()

        # Check if amount is a valid number
        if not amount.replace(".", "", 1).isdigit():
            print("Invalid amount. Please try again.")
            time.sleep(IDLE_TIME)
            return self._validate_expense_amount()

        # Convert to float and format to 2 decimal places
        return f"{float(amount):.2f}"

    def _get_updated_values(self, detail_choice, transaction):
        """Get updated values for transaction editing."""
        values = {
            'amount': transaction['amount'],
            'date': transaction['date'],
            'category': transaction['category'],
            'remarks': transaction['remarks']
        }

        if detail_choice == "1":
            amount_input = self._validate_expense_amount()
            if amount_input is None:
                return None
            values['amount'] = f"{float(amount_input):.2f}"

        elif detail_choice == "2":
            date_input = input("Enter new date (DD/MM/YYYY) or \"cancel\": ")
            if date_input == "cancel":
                return None
            values['date'] = date_input

        elif detail_choice == "3":
            category_input = self._get_categories(transaction['type'])
            if category_input == "cancel":
                return None
            values['category'] = category_input

        elif detail_choice == "4":
            remark_input = input("Enter new remark (or \"cancel\" to go back): ")
            if remark_input == "cancel":
                return None
            values['remarks'] = remark_input

        return values

    def _confirm_deletion(self, transaction_type):
        """Confirm transaction deletion."""
        confirm = input(f"\nAre you sure you want to delete this {transaction_type}? (yes/no): ").lower()
        if confirm not in ["yes", "y"]:
            print(f"\n{transaction_type.capitalize()} deletion cancelled.")
            time.sleep(IDLE_TIME)
            return False
        return True

    def _get_categories(self, transaction_type):
        """Get the appropriate categories for the transaction type."""
        categories = self.categories.get_category_list(transaction_type)
        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")

        category_choice = input(f"Choose a category (1-{len(categories)}) or \"cancel\" to go back: ")

        # Input validation
        if not category_choice.isdigit() or int(category_choice) < 1 or int(category_choice) > len(categories):
            print("Invalid choice. Please try again.")
            time.sleep(IDLE_TIME)
            return self._get_categories(transaction_type)

        return categories[int(category_choice) - 1]
