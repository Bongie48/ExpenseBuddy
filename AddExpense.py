from flask import Flask, render_template, request, redirect, url_for, flash
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Route to display the form
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        amount_str = request.form.get('amount', '').strip()
        date_str = request.form.get('date', '').strip()
        description = request.form.get('description', '').strip()

        # Validate inputs
        errors = []

        if not category:
            errors.append("Category is required.")
        if not amount_str:
            errors.append("Amount is required.")
        else:
            try:
                amount = float(amount_str)
            except ValueError:
                errors.append("Please enter a valid number for the amount.")
        if not date_str:
            errors.append("Date is required.")
        else:
            try:
                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
            except ValueError:
                errors.append("Please enter a valid date in MM/DD/YYYY format.")

        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for('add_expense'))

        # Save to CSV
        with open('ExpenseRecord.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([category, amount, date_obj.date(), description])

        flash("Expense record added successfully!")
        return redirect(url_for('add_expense'))

    return render_template('add_expense.html')