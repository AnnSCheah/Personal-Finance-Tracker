"""Module for handling report generation and display in the budget tracking application."""

from transactions import get_total, view_filtered_transactions

def get_financial_summary():
    """Calculate and return financial summary data."""
    income = float(get_total("income"))
    expenses = float(get_total("expense"))
    balance = income - expenses
    return {
        "income": income,
        "expenses": expenses,
        "balance": balance
    }

def display_financial_summary():
    """Display formatted financial summary."""
    summary = get_financial_summary()
    print("\nFinancial Summary")
    print("-----------------")
    print(f"Total Income: ${summary['income']:.2f}")
    print(f"Total Expenses: ${summary['expenses']:.2f}")
    print(f"Net Balance: ${summary['balance']:.2f}")
