"""Command-line interface for the budget tracking application."""

from menu_manager import MenuManager
from display_manager import DisplayManager
from transaction_ui import TransactionUI
from reports import display_financial_summary, view_expenses, view_income

class BudgetApp:
    def __init__(self):
        self.display = DisplayManager()
        self.menu = MenuManager()
        self.transaction_ui = TransactionUI(self.display)
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

    def add_expense(self):
        """Add an expense transaction."""
        return self.transaction_ui.add_transaction_ui("expense")

    def add_income(self):
        """Add an income transaction."""
        return self.transaction_ui.add_transaction_ui("income")

    def edit_expense(self):
        """Edit an expense transaction."""
        return self.transaction_ui.edit_transaction_ui("expense")

    def edit_income(self):
        """Edit an income transaction."""
        return self.transaction_ui.edit_transaction_ui("income")

    def delete_expense(self):
        """Delete an expense transaction."""
        return self.transaction_ui.delete_transaction_ui("expense")

    def delete_income(self):
        """Delete an income transaction."""
        return self.transaction_ui.delete_transaction_ui("income")

    def view_transactions(self, transaction_type):
        """Generic view method for transactions."""
        self.display.clear()
        if transaction_type == "expense":
            view_expenses()
        else:
            view_income()
        input("\nPress Enter to continue...")
        return self.view_reports()

    def view_expenses_ui(self):
        """View all expenses."""
        return self.view_transactions("expense")

    def view_income_ui(self):
        """View all income."""
        return self.view_transactions("income")

    def view_balance(self):
        """View financial summary."""
        self.display.clear()
        display_financial_summary()
        input("\nPress Enter to continue...")
        return self.view_reports()

    def delete_all_transactions(self):
        """Delete all transactions."""
        return self.transaction_ui.delete_all_transactions()

    def exit_app(self):
        """Exit the application."""
        self.display.clear()
        print("Thank you for using the Budget App!")
        exit()

if __name__ == "__main__":
    app = BudgetApp()
    app.main()