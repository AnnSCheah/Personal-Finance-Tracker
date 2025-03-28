"""Module for managing display formatting and screen operations."""

import os

class DisplayManager:
    def clear(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_transaction_details(self, amount, date, category, remarks):
        """Display transaction details in a formatted way."""
        print(f"Amount: ${amount}")
        print(f"Date: {date}")
        print(f"Category: {category}")
        print(f"Remark: {remarks}")

    def show_filtered_transactions(self, transactions, transaction_type):
        """Display filtered transactions and return if any exist."""
        transactions_exist = False
        for transaction in transactions:
            if transaction.get("type", "expense") == transaction_type:
                transactions_exist = True
                print(f"ID: {transaction['id']}")
                # Extract only the required fields for show_transaction_details
                details = {
                    'amount': transaction['amount'],
                    'date': transaction['date'],
                    'category': transaction['category'],
                    'remarks': transaction['remarks']
                }
                self.show_transaction_details(**details)
                print("")

        if not transactions_exist:
            print(f"No {transaction_type} transactions found.")
            print("")

        return transactions_exist

    def show_edit_menu(self, transaction, transaction_type):
        """Display the edit menu for a transaction."""
        print(f"Current {transaction_type} details:")
        print(f"1. Amount: ${transaction['amount']}")
        print(f"2. Date: {transaction['date']}")
        print(f"3. Category: {transaction['category']}")
        print(f"4. Remark: {transaction['remarks']}")
        print("5. Go back")
        print("")

    def show_category_menu(self, categories):
        """Display the category menu for a transaction."""
        count = 1
        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")
            count += 1
        print(f"{count}. Go back")
        print("")