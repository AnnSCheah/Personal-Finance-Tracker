"""Module for managing menu configurations and display."""

import time

class MenuManager:
    def __init__(self):
        self.main_menu = {}
        self.transaction_menu = {}
        self.reports_menu = {}
        self.categories_menu = {}
        self.exit_handler = None

    def initialize_menus(self, handlers):
        """Initialize menu configurations with function references."""
        self.exit_handler = handlers.exit_app

        self.main_menu.update({
            "1": ("Manage Transactions", handlers.manage_transactions),
            "2": ("View Reports", handlers.view_reports),
            "3": ("Manage Categories", handlers.manage_categories),
            "4": ("Exit", handlers.exit_app)
        })

        self.transaction_menu.update({
            "1": ("Add Expense", lambda:handlers.add_transaction("expense")),
            "2": ("Add Income", lambda:handlers.add_transaction("income")),
            "3": ("Edit Expense", lambda:handlers.edit_transaction("expense")),
            "4": ("Edit Income", lambda:handlers.edit_transaction("income")),
            "5": ("Delete Expense", lambda:handlers.delete_transaction("expense")),
            "6": ("Delete Income", lambda:handlers.delete_transaction("income")),
            "7": ("Go Back", handlers.main)
        })

        self.reports_menu.update({
            "1": ("View All Expenses", lambda:handlers.view_transactions("expense")),
            "2": ("View All Income", lambda:handlers.view_transactions("income")),
            "3": ("View Financial Summary", handlers.view_balance),
            "4": ("Delete All Transactions", handlers.delete_all_transactions),
            "5": ("Go Back", handlers.main)
        })

        self.categories_menu.update({
            "1": ("Add Expense Category", lambda:handlers.add_category("expense")),
            "2": ("Add Income Category", lambda:handlers.add_category("income")),
            "3": ("Edit Expense Category", lambda:handlers.edit_category("expense")),
            "4": ("Edit Income Category", lambda:handlers.edit_category("income")),
            "5": ("Delete Expense Category", lambda:handlers.delete_category("expense")),
            "6": ("Delete Income Category", lambda:handlers.delete_category("income")),
            "7": ("Go Back", handlers.main)
        })

    def display_menu(self, title, menu_items):
        """Display a menu with the given title and items."""
        print(f"\n{title}")
        print("-----------------")
        for key, (label, _) in menu_items.items():
            print(f"{key}. {label}")

    def handle_menu_choice(self, menu_items, choice, return_to):
        """Handle user's menu choice."""
        if choice == "exit":
            return self.exit_handler()

        if not choice.isdigit() or choice not in menu_items:
            print("Invalid choice. Please try again.")
            time.sleep(0.5)
            return return_to()

        _, function = menu_items[choice]
        result = function()

        # Handle menu transitions
        if result in ["manage_transactions", "manage_categories"]:
            return return_to()  # Return to the previous menu (manage transactions)
        elif result == "main":
            return self.main_menu["1"][1]()  # Return to main menu

        return result