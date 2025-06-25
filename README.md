ExpenseBuddy

ExpenseBuddy is a simple, user-friendly web application for tracking, managing, and visualizing your personal expenses and monthly budgets. Built with Flask and Bootstrap, it helps you stay on top of your finances with ease.

## Features
Add Expenses: Quickly log your daily expenses with category, amount, date, and description.
View Expenses: See all your expenses in a clean, sortable table, grouped by month with monthly totals.
Monthly Budget: Set and manage your monthly budget, add budget items, and mark them as completed ("scratch" them) with a click.
Reports: Generate and download PDF reports of your expenses.
User Authentication: Simple login system for personal use.
Responsive Design: Works well on desktop and mobile devices.



Getting Started

Prerequisites

- Python 3.8+
- pip

Installation

1. Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ExpenseBuddy.git
    cd ExpenseBuddy
    ```

2. Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:**
    ```bash
    python app.py
    ```

4. Open your browser and go to:**
    ```
    http://127.0.0.1:5000/
    ```

File Structure

```
ExpenseBuddy/
├── app.py
├── requirements.txt
├── ExpenseRecord.csv
├── MonthlyBudget.csv
├── users.csv
├── /templates
│   ├── home.html
│   ├── add.html
│   ├── view.html
│   ├── view_by_category.html
│   ├── budget.html
│   ├── report.html
│   └── navbar.html
└── /static
    └── (optional: custom CSS/JS)
```

Usage

- Add Expense: Use the "Add Expense" page to log new expenses.
- View Expenses: Go to "View Expenses" to see all your expenses, grouped by month.
- Budget: Set your monthly budget and add items. Click an item to mark it as completed.
- Reports: Download a PDF report of your expenses from the "Reports" page.

Customization

- You can change categories, styling, and add more features as needed.
- All data is stored in CSV files for simplicity.

License

This project is licensed under the MIT License.

---

enjoy using ExpenseBuddy!
