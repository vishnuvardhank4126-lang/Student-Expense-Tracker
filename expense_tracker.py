"""Core operations for the student expense tracker."""

from math import isfinite
from typing import TypedDict


CATEGORIES = ("Food", "Travel", "Education", "Others")


class Expense(TypedDict):
    """The fields stored for one expense."""

    id: int
    amount: float
    category: str
    description: str


def validate_expense_amount(amount: float) -> None:
    """Validate that an expense amount is finite and greater than zero.

    Description:
        Reject zero, negative, non-finite, and non-numeric amount values.
    Args:
        amount: Expense amount to validate.
    Returns:
        None when the amount is valid.
    Raises:
        ValueError: If the amount is not a finite positive number.
    """
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("Expense amount must be a finite number greater than zero.")
    try:
        is_finite = isfinite(amount)
    except OverflowError:
        is_finite = False
    if not is_finite or amount <= 0:
        raise ValueError("Expense amount must be a finite number greater than zero.")


def validate_expense_amount_and_category(amount: float, category: str) -> None:
    """Validate an expense amount and category.

    Description:
        Check that the amount is finite and positive and that the category is
        one of the tracker's supported categories.
    Args:
        amount: Expense amount to validate.
        category: Category name to validate.
    Returns:
        None when both values are valid.
    Raises:
        ValueError: If the amount or category is invalid.
    """
    validate_expense_amount(amount)
    if not category.strip():
        raise ValueError("Category cannot be empty.")
    if category not in CATEGORIES:
        raise ValueError(f"Category must be one of: {', '.join(CATEGORIES)}.")


def add_expense(
    expenses: list[Expense], amount: float, category: str, description: str
) -> Expense:
    """Add a validated expense to the tracker.

    Description:
        Assign the next available ID, round the amount to two decimals, and
        append the new record to the expense list.
    Args:
        expenses: Mutable list of expense records to update.
        amount: Positive finite amount to record.
        category: Supported expense category.
        description: Non-empty description of the expense.
    Returns:
        The added expense record; its ID confirms the addition.
    Raises:
        ValueError: If the amount, category, or description is invalid.
    """
    validate_expense_amount_and_category(amount, category)
    if not description.strip():
        raise ValueError("Description cannot be empty.")

    rounded_amount = round(float(amount), 2)
    validate_expense_amount(rounded_amount)
    expense_id = max((expense["id"] for expense in expenses), default=0) + 1
    expense: Expense = {
        "id": expense_id,
        "amount": rounded_amount,
        "category": category,
        "description": description.strip(),
    }
    expenses.append(expense)
    return expense


def display_expenses(expenses: list[Expense]) -> str:
    """Format all expenses as readable text.

    Description:
        Create a table containing each expense, or an empty-state message.
    Args:
        expenses: Expense records to display.
    Returns:
        A formatted table or a message when there are no expenses.
    """
    if not expenses:
        return "No expenses recorded."

    rows = ["ID | Amount | Category | Description", "-" * 56]
    for expense in expenses:
        rows.append(
            f"{expense['id']} | {expense['amount']:.2f} | "
            f"{expense['category']} | {expense['description']}"
        )
    return "\n".join(rows)


def calculate_total(expenses: list[Expense]) -> float:
    """Calculate the total of all valid expenses.

    Description:
        Validate every stored amount, then sum the amounts rounded to cents.
    Args:
        expenses: Expense records whose amounts should be totaled.
    Returns:
        Total expense amount rounded to two decimal places; zero for an empty
        list.
    Raises:
        ValueError: If any stored amount is invalid.
    """
    for expense in expenses:
        validate_expense_amount(expense["amount"])
    return round(sum(expense["amount"] for expense in expenses), 2)


def search_by_category(expenses: list[Expense], category: str) -> list[Expense]:
    """Search expenses by category.

    Description:
        Find records whose category matches the requested category, ignoring
        letter case.
    Args:
        expenses: Expense records to search.
        category: Category name to match.
    Returns:
        A list of matching expense records, or an empty list if none match.
    """
    normalized_category = category.strip().casefold()
    return [
        expense
        for expense in expenses
        if expense["category"].casefold() == normalized_category
    ]


def delete_expense(expenses: list[Expense], expense_id: int) -> bool:
    """Delete an expense from the tracker by ID.

    Description:
        Remove the first record with the requested ID from the mutable list.
    Args:
        expenses: Mutable list of expense records to update.
        expense_id: ID of the expense to delete.
    Returns:
        True if a record was deleted; otherwise, False.
    """
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            del expenses[index]
            return True
    return False


def generate_summary(expenses: list[Expense]) -> str:
    """Generate a spending summary for all recorded expenses.

    Description:
        Report the overall total and a subtotal for every supported category.
    Args:
        expenses: Expense records to summarize.
    Returns:
        Formatted total and category subtotals, or an empty-state message.
    Raises:
        ValueError: If any stored expense amount is invalid.
    """
    if not expenses:
        return "No expenses recorded."

    lines = [f"Total expenses: {calculate_total(expenses):.2f}", "By category:"]
    for category in CATEGORIES:
        category_total = calculate_total(search_by_category(expenses, category))
        lines.append(f"  {category}: {category_total:.2f}")
    return "\n".join(lines)