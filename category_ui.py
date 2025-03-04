import json
import os
import time

class CategoryUI:
    def __init__(self, display_manager):
        self.display = display_manager
        self.CATEGORIES_FILE = "categories.json"
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
        category_name = input(f"Enter the {category_type} category name (type \"cancel\" to go back): ")

        if category_name in ["cancel"]:
            return "manage_categories"

        self.categories[category_type].append(category_name)
        self._save_categories(self.categories)

        print(f"\n{category_name} added to {category_type} categories.")

        input("\nPress Enter to continue...")
        return "manage_categories"

    def edit_category_ui(self, category_type="expense"):
        """Handle UI for editing a category."""
        self.display.clear()
        print(f"Edit {category_type.capitalize()} Category")
        print("----------------------")

        # Check if there are any existing categories to edit.
        if not self.categories[category_type]:
            print(f"No {category_type} categories exist!.")
            input("\nPress Enter to continue...")
            return "manage_categories"

        self.display.show_category_menu(self.categories[category_type])
        edit_choice = input(f"Enter the number of the category to edit (1-{len(self.categories[category_type]) + 1}): ")

        # Input validation
        if not edit_choice.isdigit() or int(edit_choice) < 1 or int(edit_choice) > len(self.categories[category_type]) + 1:
            print("Invalid choice. Please try again.")
            time.sleep(0.5)
            return self.edit_category_ui(category_type)

        # Check if user wants to cancel the operation.
        if int(edit_choice) == len(self.categories[category_type]) + 1:
            return "manage_categories"

        new_category_name = input(f"Enter the new {category_type} category name for \"{self.categories[category_type][int(edit_choice) - 1]}\". (type \"cancel\" to go back): ")

        # Input validation
        if not new_category_name:
            print("Category name cannot be empty. Please try again.")
            input("\nPress Enter to continue...")
            return self.edit_category_ui(category_type)

        # Check if the user wants to cancel the operation.
        if new_category_name in ["cancel"]:
            return "manage_categories"

        # Check if the new category name is the same as the old one.
        if new_category_name == self.categories[category_type][int(edit_choice) - 1]:
            print(f"{new_category_name} is the same as the old category name.")
            input("\nPress Enter to continue...")
            return self.edit_category_ui(category_type)

        # Check if the new category name already exists.
        if new_category_name in self.categories[category_type]:
            print(f"{new_category_name} already exists in {category_type} categories.")
            input("\nPress Enter to continue...")
            return self.edit_category_ui(category_type)

        # Get the old category name for feedback
        old_category_name = self.categories[category_type][int(edit_choice) - 1]
        self.categories[category_type][int(edit_choice) - 1] = new_category_name
        self._save_categories(self.categories)

        print(f"\nCategory updated successfully!")
        print(f"{old_category_name} updated to {new_category_name} in {category_type} categories.")

        input("\nPress Enter to continue...")
        return "manage_categories"