"""Command-line interface for the student expense tracker."""

from math import isfinite

from expense_tracker import (
    CATEGORIES,
    Expense,
    add_expense,
    calculate_total,
    delete_expense,
    display_expenses,
    generate_summary,
    search_by_category,
)


def read_positive_amount() -> float:
    """Prompt until the user enters a valid positive amount.

    Description:
        Read a finite numeric amount greater than zero, repeating after invalid
        input.
    Args:
        None.
    Returns:
        The validated amount as a float.
    """
    while True:
        try:
            amount = float(input("Amount (for example, 12.50): ").strip())
            if not isfinite(amount) or amount <= 0:
                print("Amount must be a finite number greater than zero.")
                continue
            return amount
        except ValueError:
            print("Enter a valid amount, for example 12.50.")


def choose_category() -> str:
    """Prompt until the user selects a supported category.

    Description:
        Display available categories and accept a match regardless of letter
        case.
    Args:
        None.
    Returns:
        The selected category using its standard capitalization.
    """
    print("Categories:", ", ".join(CATEGORIES))
    while True:
        category = input("Category: ").strip().casefold()
        for valid_category in CATEGORIES:
            if category == valid_category.casefold():
                return valid_category
        print("Choose one of the listed categories.")


def read_expense_id() -> int:
    """Prompt until the user enters a positive whole-number ID.

    Description:
        Repeat the prompt after non-numeric or non-positive input.
    Args:
        None.
    Returns:
        The validated expense ID.
    """
    while True:
        try:
            expense_id = int(input("Expense ID: "))
            if expense_id > 0:
                return expense_id
            print("ID must be a positive whole number.")
        except ValueError:
            print("Enter a valid whole-number ID.")


def show_menu() -> None:
    """Run the interactive expense tracker menu.

    Description:
        Handle menu selections for adding, displaying, totaling, searching,
        deleting, and summarizing expenses until the user exits.
    Args:
        None.
    Returns:
        None. The function runs the interactive command-line session.
    """
    expenses: list[Expense] = []

    while True:
        print(
            "\n====================================\n"
            "       STUDENT EXPENSE TRACKER\n"
            "====================================\n"
            "1. Add an expense\n"
            "2. Display all expenses\n"
            "3. Show total expenses\n"
            "4. Search expenses by category\n"
            "5. Delete an expense by ID\n"
            "6. Generate an expense summary\n"
            "0. Exit the tracker"
        )
        choice = input("Select an option (0-6): ").strip()

        if choice == "1":
            amount = read_positive_amount()
            category = choose_category()
            description = input("Description: ").strip()
            while not description:
                print("Description cannot be empty.")
                description = input("Description: ").strip()
            expense = add_expense(expenses, amount, category, description)
            print(f"Expense added with ID {expense['id']}.")
        elif choice == "2":
            print(display_expenses(expenses))
        elif choice == "3":
            print(f"Total expenses: {calculate_total(expenses):.2f}")
        elif choice == "4":
            category = choose_category()
            print(display_expenses(search_by_category(expenses, category)))
        elif choice == "5":
            expense_id = read_expense_id()
            if delete_expense(expenses, expense_id):
                print("Expense deleted.")
            else:
                print("No expense found with that ID.")
        elif choice == "6":
            print(generate_summary(expenses))
        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Enter a menu option from 0 to 6.")


if __name__ == "__main__":
    show_menu()