"""Command-line interface for the budget tracking application."""

from menu_manager import MenuManager
from display_manager import DisplayManager
from transaction_ui import TransactionUI
from category_ui import CategoryUI
from reports import display_financial_summary
from transactions import view_filtered_transactions

class BudgetApp:
    def __init__(self):
        self.display = DisplayManager()
        self.menu = MenuManager()
        self.transaction_ui = TransactionUI(self.display)
        self.category_ui = CategoryUI(self.display)
        self.menu.initialize_menus(self)

    def main(self):
        """Main menu of the application."""
        self.display.clear()
        print("Welcome to the Budget App!")

        display_financial_summary()
        self.menu.display_menu("Main Menu:", self.menu.main_menu)

        choice = input("\nEnter your choice: ")
        self.menu.handle_menu_choice(self.menu.main_menu, choice, self.main)

    def manage_transactions(self):
        """Transaction management menu."""
        self.display.clear()

        self.menu.display_menu("Manage Transactions", self.menu.transaction_menu)

        choice = input("\nEnter your choice: ")
        self.menu.handle_menu_choice(self.menu.transaction_menu, choice, self.manage_transactions)

    def view_reports(self):
        """Reports menu."""
        self.display.clear()

        self.menu.display_menu("View Reports", self.menu.reports_menu)

        choice = input("\nEnter your choice: ")
        self.menu.handle_menu_choice(self.menu.reports_menu, choice, self.view_reports)

    def manage_categories(self):
        """Category management menu."""
        self.display.clear()

        self.menu.display_menu("Manage Categories", self.menu.categories_menu)

        choice = input("\nEnter your choice: ")
        self.menu.handle_menu_choice(self.menu.categories_menu, choice, self.manage_categories)

    def add_transaction(self, transaction_type):
        """Add an expense transaction."""
        return self.transaction_ui.add_transaction_ui(transaction_type)

    def edit_transaction(self, transaction_type):
        """Edit an expense transaction."""
        return self.transaction_ui.edit_transaction_ui(transaction_type)

    def delete_transaction(self, transaction_type):
        """Delete an expense transaction."""
        return self.transaction_ui.delete_transaction_ui(transaction_type)

    def view_transactions(self, transaction_type):
        """Generic view method for transactions."""
        self.display.clear()
        view_filtered_transactions("expense") if transaction_type == "expense" else view_filtered_transactions("income")

        input("\nPress Enter to continue...")
        return self.view_reports()

    def view_balance(self):
        """View financial summary."""
        self.display.clear()
        display_financial_summary()
        input("\nPress Enter to continue...")
        return self.view_reports()

    def delete_all_transactions(self):
        """Delete all transactions."""
        return self.transaction_ui.delete_all_transactions()

    def add_category(self, transaction_type):
        """Add a category."""
        return self.category_ui.add_category_ui(transaction_type)

    def edit_category(self, transaction_type):
        """Edit a category."""
        return self.category_ui.edit_category_ui(transaction_type)

    def delete_category(self, transaction_type):
        """Delete a category."""
        return self.category_ui.delete_category_ui(transaction_type)

    def view_category(self):
        """View all categories"""
        return self.category_ui.view_category_ui()

    def exit_app(self):
        """Exit the application."""
        self.display.clear()
        print("Thank you for using the Budget App!")
        exit()

if __name__ == "__main__":
    app = BudgetApp()
    app.main()