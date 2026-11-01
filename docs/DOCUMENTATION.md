# AI Coding Assistant Practicum – A1

## 1. Project Information

- **Subject:** Automation in Software Development
- **Semester:** V
- **Unit:** II
- **Assignment:** A1 – AI Coding Assistant Practicum
- **Project Name:** Student Expense Tracker
- **AI Coding Assistant:** GitHub Copilot
- **Programming Language:** Python

## 2. Project Objective

The objective of this project is to develop a Student Expense Tracker using Python. It allows users to add, display, search, delete and summarize expenses. The project demonstrates the practical application of AI coding assistance and prompt engineering techniques.

## 3. Tools and Technologies

- Python 3.14.6
- Visual Studio Code
- GitHub Copilot
- Git
- GitHub
- Python unittest

## 4. Project Features

1. Add an expense.
2. Display all expenses.
3. Calculate total expenses.
4. Search expenses by category.
5. Delete expenses.
6. Generate expense summaries.
7. Validate user inputs.

## 5. Prompt Engineering Techniques

### 5.1 Zero-shot Prompting

**Purpose:** Generate the basic application without providing input-output examples.

**Prompt 1:** Create a beginner-friendly Python Student Expense Tracker with seven functions, input validation and unit tests. Generate main.py, expense_tracker.py, test_expense_tracker.py and README.md.

**Actual response:** Copilot generated the four requested files and implemented the expense management functions and command-line interface.

**Evaluation:** Accepted the generated files after reviewing them. The application launched successfully.

**Evidence:** 01_zero_shot.png

### 5.2 Few-shot Prompting

**Purpose:** Guide Copilot using explicit input-output examples.

**Prompt 2:** Improve expense validation using examples for valid amounts, negative amounts, zero amounts and empty categories. Add corresponding unit tests.

**Actual response:** Copilot added expense validation and separate tests for the examples.

**Evaluation:** Accepted the changes after reviewing the implementation. All 12 tests passed.

**Evidence:** 02_few_shot.png

### 5.3 Chain-of-thought Prompting

**Purpose:** Investigate logical errors and edge cases.

**Prompt 3:** Think step by step. Investigate empty expense lists, invalid amounts, NaN, infinity and incorrect calculations. Identify genuine bugs, fix them and run the unit tests.

**Actual response:** Copilot identified invalid amounts that could affect totals and improved validation and summary calculations.

**Evaluation:** Accepted the appropriate changes. All 14 tests passed.

**Evidence:** 03_chain_of_thought.png

## 6. Additional Prompt Log

### Prompt 4 – Zero-shot

**Task:** Improve the command-line interface.

**Prompt:** Improve the Student Expense Tracker CLI. Handle invalid menu choices, non-numeric amounts and provide confirmation messages. Preserve existing functionality and run the tests.

**Actual response:** Copilot improved the menu, input handling and confirmation messages.

**Evaluation:** Accepted the changes. All 18 tests passed.

**Evidence:** 04_cli_generation.png

### Prompt 5 – Few-shot

**Task:** Improve function documentation.

**Prompt:** Provide three examples of function descriptions, arguments and return values. Apply the same documentation style to all relevant functions.

**Actual response:** Copilot expanded docstrings in main.py and expense_tracker.py.

**Evaluation:** Accepted the documentation improvements. All 18 tests passed.

**Evidence:** 05_docstring_generation.png

### Prompt 6 – Chain-of-thought

**Task:** Perform a final code quality review.

**Prompt:** Think step by step. Inspect expense validation, invalid IDs, missing categories and empty lists. Identify genuine bugs, explain their causes, fix necessary issues and run all tests.

**Actual response:** Copilot improved amount validation by checking rounded values before adding expenses and added regression tests.

**Evaluation:** Accepted the appropriate changes. All 21 tests passed.

09-final-code-review-21-tests.jpg

## 7. Testing Results

| Testing stage | Result |
|---|---|
| Initial unit tests | 8 passed |
| Few-shot validation | 12 passed |
| Chain-of-thought debugging | 14 passed |
| CLI improvements | 18 passed |
| Documentation improvements | 18 passed |
| Final code review | 21 passed |

The application was successfully launched using `python main.py`. The tests were executed using `python -m unittest -v`.

## 8. Reflection

Using GitHub Copilot for this project helped me understand how AI coding assistants can support software development. It generated the initial project structure and implemented the main expense management functions quickly. This reduced the time required to write repetitive code manually.

Zero-shot prompting was useful for generating the initial application because the requirements were clear. Few-shot prompting helped improve input validation and documentation by providing examples of the expected output. Chain-of-thought prompting was useful for investigating edge cases, identifying logical problems and improving the reliability of the application.

Copilot was particularly useful for generating code, suggesting improvements and creating unit tests. However, its output still required review and testing. Some generated changes needed to be checked to ensure that existing functionality was preserved.

Compared with other AI coding assistants discussed in class, such as Cursor, Amazon Q Developer and Gemini Code Assist, Copilot provided a convenient experience within Visual Studio Code. A direct hands-on comparison with those tools was not performed in this project.

In a real software development team, I would choose Copilot when working in VS Code and when I need quick code generation, debugging assistance and test suggestions. This assignment helped me understand that effective prompting and human verification are both important when using AI in software development.

## 9. Conclusion

The Student Expense Tracker demonstrates how AI coding assistants and prompt engineering techniques can support the development, testing and improvement of a Python application.

## 10. Repository Link

GitHub Repository: [Paste your actual GitHub repository URL here]
