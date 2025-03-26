import json
import os
import time
from src.utils.settings import CATEGORIES_FILE, IDLE_TIME

class CategoryUI:
    def __init__(self, display_manager):
        self.display = display_manager
        self.CATEGORIES_FILE = CATEGORIES_FILE
        print(f"File path: {self.CATEGORIES_FILE}")
        self._load_categories()

    def _load_categories(self):
        if not os.path.exists(self.CATEGORIES_FILE):
            self._save_categories({"expense": [], "income": []})
        with open(self.CATEGORIES_FILE, "r", encoding='utf-8') as file:
            self.categories = json.load(file)

    def _save_categories(self, categories):
        with open(self.CATEGORIES_FILE, "w", encoding='utf-8') as file:
            json.dump(categories, file, indent=4)

    def get_category_list(self, category_type):
        return self.categories[category_type]

    def add_category_ui(self, category_type="expense"):
        """Handle UI for adding a category."""
        self.display.clear()
        print(f"Add {category_type} Category")
        print("----------------------")

        category_list = self.categories[category_type]

        # Display existing categories
        print(f"Existing {category_type} categories:")
        for category in category_list:
            print(f"- {category}")
        print("")

        category_name = input(f"Enter the {category_type} category name (type \"cancel\" to go back): ")

        # Validate input
        if not self._validate_category_name(category_type, category_name):
            return self.add_category_ui(category_type)

        # Check if the user wants to cancel the operation
        if category_name in ["cancel"]:
            return "manage_categories"

        category_list.append(category_name)
        self._save_categories(self.categories)

        print(f"\n{category_name} added to {category_type} categories.")

        input("\nPress Enter to continue...")
        return "manage_categories"

    def edit_category_ui(self, category_type="expense"):
        """Handle UI for editing a category."""
        self.display.clear()
        print(f"Edit {category_type.capitalize()} Category")
        print("----------------------")

        category_list = self.categories[category_type]

        # Check if there are any existing categories to edit.
        if not category_list:
            print(f"No {category_type} categories exist!.")
            input("\nPress Enter to continue...")
            return "manage_categories"

        self.display.show_category_menu(category_list)
        edit_choice = input(f"Enter the number of the category to edit (1-{len(category_list) + 1}): ")

        # Validate input
        if not self._validate_category_index(category_list, edit_choice):
            return self.edit_category_ui(category_type)

        # Check if user wants to go back
        if int(edit_choice) == len(category_list) + 1:
            return "manage_categories"

        new_category_name = input(f"Enter the new {category_type} category name for \"{category_list[int(edit_choice) - 1]}\". (type \"cancel\" to go back): ")

        # Validate input
        if not self._validate_category_name(edit_choice, category_type, new_category_name):
            return self.edit_category_ui(category_type)

        # Get the old category name for feedback
        old_category_name = category_list[int(edit_choice) - 1]
        category_list[int(edit_choice) - 1] = new_category_name
        self._save_categories(self.categories)

        print(f"\nCategory updated successfully!")
        print(f"{old_category_name} updated to {new_category_name} in {category_type} categories.")

        input("\nPress Enter to continue...")
        return "manage_categories"

    def delete_category_ui(self, category_type="expense"):
        """Handle UI for deleting a category."""
        self.display.clear()
        print(f"Delete {category_type.capitalize()} Category")
        print("----------------------")

        category_list = self.categories[category_type]

        # Check if there are any existing categories to delete.
        if not self.categories[category_type]:
            print(f"No {category_type} categories exist!.")
            input("\nPress Enter to continue...")
            return "manage_categories"

        self.display.show_category_menu(category_list)
        delete_choice = input(f"Enter the number of the category to delete (1-{len(category_list) + 1}): ")

        # Input validation
        if not self._validate_category_index(category_list, delete_choice):
            return self.delete_category_ui(category_type)

        # Check if user wants to go back
        if int(delete_choice) == len(category_list) + 1:
            return "manage_categories"

        # Get the category name for feedback
        category_name = category_list.pop(int(delete_choice) - 1)
        self._save_categories(self.categories)

        print(f"\nCategory deleted successfully!")
        print(f"{category_name} removed from {category_type} categories.")
        input("\nPress Enter to continue...")
        return "manage_categories"

    def view_category_ui(self):
        """List out the categories for expense & income"""
        expense_cat = self.categories["expense"]
        income_cat = self.categories["income"]

        self.display.clear()
        print("Expense Categories")
        print("----------------------")
        for category in expense_cat:
            print(f"- {category}")

        print("")
        print("Income Categories")
        print("----------------------")
        for category in income_cat:
            print(f"- {category}")
        print("")
        input("\nPress Enter to continue...")
        return "manage_categories"

    def _validate_category_index(self, category_list, category_index):
        # Check if input is empty
        if not category_index:
            print("Input cannot be empty. Please try again.")
            time.sleep(IDLE_TIME)
            return False

        # Input validation
        if not category_index.isdigit() or int(category_index) < 1 or int(category_index) > len(category_list) + 1:
            print("Invalid choice. Please try again.")
            time.sleep(IDLE_TIME)
            return False

        return True

    def _validate_category_name(self, category_type, category_name, choice=None):
        # Check if input is empty
        if not category_name:
            print("Category name cannot be empty. Please try again.")
            time.sleep(IDLE_TIME)
            return False

        # Will only run if the user is editing a category.
        if choice:
            # Check if the new category name is the same as the old one.
            if category_name == self.categories[category_type][int(choice) - 1]:
                print(f"{category_name} is the same as the old category name.")
                time.sleep(IDLE_TIME)
                return False

        # Check if the new category name already exists.
        if category_name in self.categories[category_type]:
            print(f"{category_name} already exists in {category_type} categories.")
            time.sleep(IDLE_TIME)
            return False

        return True