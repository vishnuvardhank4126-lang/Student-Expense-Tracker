"""Unit tests for the student expense tracker operations."""

from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from expense_tracker import (
    add_expense,
    calculate_total,
    delete_expense,
    display_expenses,
    generate_summary,
    search_by_category,
    validate_expense_amount_and_category,
)
from main import show_menu


class ExpenseTrackerTests(unittest.TestCase):
    """Check expense creation, lookup, totals, deletion, and empty states."""

    def setUp(self) -> None:
        self.expenses = []
        add_expense(self.expenses, 12.50, "Food", "Lunch")
        add_expense(self.expenses, 25.00, "Travel", "Bus pass")
        add_expense(self.expenses, 8.25, "Food", "Coffee")

    def test_example_accepts_positive_amount_and_supported_category(self) -> None:
        validate_expense_amount_and_category(50, "Food")

    def test_example_rejects_negative_amount(self) -> None:
        with self.assertRaisesRegex(ValueError, "amount"):
            validate_expense_amount_and_category(-20, "Travel")

    def test_example_rejects_zero_amount(self) -> None:
        with self.assertRaisesRegex(ValueError, "amount"):
            validate_expense_amount_and_category(0, "Books")

    def test_example_rejects_empty_category(self) -> None:
        with self.assertRaisesRegex(ValueError, "Category cannot be empty"):
            validate_expense_amount_and_category(100, "")

    def test_add_expense_assigns_id_and_normalizes_description(self) -> None:
        expense = add_expense(self.expenses, 10, "Education", "  Notebook  ")
        self.assertEqual(expense["id"], 4)
        self.assertEqual(expense["description"], "Notebook")
        self.assertEqual(expense["amount"], 10.00)

    def test_add_expense_rejects_non_positive_amount(self) -> None:
        for amount in (0, -1, float("nan"), float("inf"), -float("inf")):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    add_expense(self.expenses, amount, "Food", "Lunch")

    def test_add_expense_rejects_amount_that_rounds_to_zero(self) -> None:
        expenses = []
        with self.assertRaisesRegex(ValueError, "amount"):
            add_expense(expenses, 0.001, "Food", "Tiny expense")
        self.assertEqual(expenses, [])

    def test_add_expense_rejects_invalid_category_and_blank_description(self) -> None:
        with self.assertRaises(ValueError):
            add_expense(self.expenses, 1, "Rent", "Room")
        with self.assertRaises(ValueError):
            add_expense(self.expenses, 1, "Food", "   ")

    def test_display_and_total(self) -> None:
        displayed = display_expenses(self.expenses)
        self.assertIn("Lunch", displayed)
        self.assertEqual(calculate_total(self.expenses), 45.75)

    def test_calculate_total_rejects_invalid_stored_amounts(self) -> None:
        invalid_amounts = (-5.0, 0.0, float("nan"), float("inf"), "12.00")
        for invalid_amount in invalid_amounts:
            with self.subTest(amount=invalid_amount):
                invalid_expense = {
                    "id": 4,
                    "amount": invalid_amount,
                    "category": "Food",
                    "description": "Invalid record",
                }
                with self.assertRaisesRegex(ValueError, "amount"):
                    calculate_total(self.expenses + [invalid_expense])

    def test_generate_summary_rejects_invalid_stored_amount(self) -> None:
        invalid_expense = {
            "id": 4,
            "amount": -5.0,
            "category": "Food",
            "description": "Invalid record",
        }
        with self.assertRaisesRegex(ValueError, "amount"):
            generate_summary(self.expenses + [invalid_expense])

    def test_search_is_case_insensitive(self) -> None:
        matching = search_by_category(self.expenses, "food")
        self.assertEqual(len(matching), 2)

    def test_search_for_missing_category_returns_empty_list(self) -> None:
        self.assertEqual(search_by_category(self.expenses, "Books"), [])

    def test_delete_by_id(self) -> None:
        self.assertTrue(delete_expense(self.expenses, 2))
        self.assertFalse(delete_expense(self.expenses, 2))
        self.assertEqual(len(self.expenses), 2)

    def test_delete_with_invalid_id_does_not_change_expenses(self) -> None:
        original_expenses = self.expenses.copy()
        for expense_id in (-1, 999, "1"):
            with self.subTest(expense_id=expense_id):
                self.assertFalse(delete_expense(self.expenses, expense_id))
        self.assertEqual(self.expenses, original_expenses)

    def test_empty_list_messages_and_total(self) -> None:
        self.assertEqual(display_expenses([]), "No expenses recorded.")
        self.assertEqual(generate_summary([]), "No expenses recorded.")
        self.assertEqual(calculate_total([]), 0)

    def test_summary_includes_totals_by_category(self) -> None:
        summary = generate_summary(self.expenses)
        self.assertIn("Total expenses: 45.75", summary)
        self.assertIn("Food: 20.75", summary)
        self.assertIn("Travel: 25.00", summary)


class ExpenseTrackerCliTests(unittest.TestCase):
    """Check menu interaction and user-facing CLI messages."""

    def run_cli(self, inputs: list[str]) -> str:
        """Run the menu with scripted input and capture its output."""
        output = StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
            show_menu()
        return output.getvalue()

    def test_menu_explains_options_and_handles_invalid_choice(self) -> None:
        output = self.run_cli(["9", "0"])
        self.assertIn("1. Add an expense", output)
        self.assertIn("0. Exit the tracker", output)
        self.assertIn("Invalid choice. Enter a menu option from 0 to 6.", output)

    def test_add_retries_after_non_numeric_amount(self) -> None:
        output = self.run_cli(["1", "not-a-number", "12.50", "Food", "Lunch", "0"])
        self.assertIn("Enter a valid amount", output)
        self.assertIn("Expense added with ID 1.", output)

    def test_add_retries_after_non_finite_amounts(self) -> None:
        output = self.run_cli(["1", "nan", "inf", "12.50", "Food", "Lunch", "0"])
        self.assertIn("Amount must be a finite number greater than zero.", output)
        self.assertIn("Expense added with ID 1.", output)

    def test_add_and_delete_show_confirmation_messages(self) -> None:
        output = self.run_cli(["1", "10", "Food", "Lunch", "5", "1", "0"])
        self.assertIn("Expense added with ID 1.", output)
        self.assertIn("Expense deleted.", output)


if __name__ == "__main__":
    unittest.main()