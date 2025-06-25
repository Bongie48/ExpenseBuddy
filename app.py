from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import csv
from collections import defaultdict, OrderedDict
from datetime import datetime
import ast
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

def read_records():
    records = []
    try:
        with open('ExpenseRecord.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                records.append(row)
    except FileNotFoundError:
        pass
    return records

def read_budget():
    try:
        with open('MonthlyBudget.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    return float(row[1])
    except FileNotFoundError:
        pass
    return None

def write_budget(month, amount):
    with open('MonthlyBudget.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([month, amount])

def get_users():
    users = {}
    if os.path.exists('users.csv'):
        with open('users.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                # row: fullname, cellphone, email, password
                if len(row) == 4:
                    users[row[2]] = {'fullname': row[0], 'cell': row[1], 'password': row[3]}
    return users

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        category = request.form['category'].strip()
        amount_str = request.form['amount'].strip()
        date_str = request.form['date'].strip()
        description = request.form['description'].strip()
        errors = []

        if not category:
            errors.append("Category is required.")
        if not amount_str:
            errors.append("Amount is required.")
        else:
            try:
                amount = float(amount_str)
            except:
                errors.append("Invalid amount.")
        if not date_str:
            errors.append("Date is required.")
        else:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                errors.append("Invalid date format (YYYY-MM-DD).")
        if errors:
            for e in errors:
                flash(e)
            return redirect(url_for('add'))

        with open('ExpenseRecord.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([category, amount, date_obj.strftime('%Y-%m-%d'), description, ""])
        flash("Record added.")
        return redirect(url_for('add'))
    return render_template('add.html')

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    from collections import defaultdict
    from datetime import datetime
    import csv

    budget_items = []
    total_budget = 0.0
    today = datetime.now()
    year = today.year
    month = today.month

    # Handle scratching (marking as completed)
    if request.method == 'POST' and 'scratch' in request.form:
        scratch_idx = int(request.form['scratch'])
        # Read all items
        try:
            with open('MonthlyBudget.csv', 'r', newline='') as f:
                reader = list(csv.reader(f))
        except FileNotFoundError:
            reader = []
        # Mark as scratched
        if 0 <= scratch_idx < len(reader):
            if len(reader[scratch_idx]) == 5:
                reader[scratch_idx][4] = 'scratched'
            elif len(reader[scratch_idx]) == 4:
                reader[scratch_idx].append('scratched')
        # Write back all items
        with open('MonthlyBudget.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(reader)
        flash("Item marked as completed!")
        return redirect(url_for('budget'))

    # Handle saving new budget items
    if request.method == 'POST' and 'scratch' not in request.form:
        item_names = request.form.getlist('item_name')
        item_prices = request.form.getlist('item_price')
        new_items = []
        for name, price in zip(item_names, item_prices):
            try:
                price_val = float(price)
            except:
                price_val = 0.0
            # Save as [name, price, year, month]
            new_items.append([name, price_val, year, month])
        # Append all items to CSV
        with open('MonthlyBudget.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for item in new_items:
                writer.writerow(item)
        flash("Monthly budget saved!")
        return redirect(url_for('budget'))

    # Load all items from CSV and group by (year, month) with global index
    grouped_items = defaultdict(list)
    try:
        with open('MonthlyBudget.csv', 'r', newline='') as f:
            reader = list(csv.reader(f))
            for idx, row in enumerate(reader):
                if len(row) >= 4:
                    name = row[0]
                    try:
                        price = float(row[1])
                        y = int(row[2])
                        m = int(row[3])
                    except ValueError:
                        continue
                    status = row[4] if len(row) > 4 else ''
                    grouped_items[(y, m)].append((name, price, status, idx))
    except FileNotFoundError:
        pass

    # Calculate total for the current month
    this_month_items = grouped_items.get((year, month), [])
    total_budget = sum(item[1] for item in this_month_items)

    return render_template(
        'budget.html',
        grouped_items=grouped_items,
        year=year,
        month=month,
        total_budget=total_budget
    )

from collections import defaultdict
from datetime import datetime

@app.route('/view')
def view():
    records = read_records()
    # Calculate total per month
    monthly_totals = defaultdict(float)
    for row in records:
        if len(row) >= 3:
            try:
                date_obj = datetime.strptime(row[2], "%Y-%m-%d")
                year_month = date_obj.strftime("%Y-%m")
                monthly_totals[year_month] += float(row[1])
            except Exception:
                continue
    # Sort by year and month
    monthly_totals = dict(sorted(monthly_totals.items()))
    return render_template(
        'view.html',
        records=records,
        monthly_totals=monthly_totals
    )

@app.route('/view_by_category')
def view_by_category():
    records = read_records()
    category_totals = defaultdict(float)
    for r in records:
        if len(r) >= 2:
            try:
                category_totals[r[0]] += float(r[1])
            except ValueError:
                continue
    return render_template('category.html', totals=category_totals)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        del_category = request.form['category']
        del_date = request.form['date']
        records = []
        try:
            with open('ExpenseRecord.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    # Only add rows that do NOT match the delete criteria
                    if len(row) >= 3 and not (row[0] == del_category and row[2] == del_date):
                        records.append(row)
        except FileNotFoundError:
            pass
        with open('ExpenseRecord.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(records)
        flash("Records deleted.")
        return redirect(url_for('delete'))
    return render_template('delete.html')

@app.route('/report')
def report():
    records = read_records()
    total_cost = 0.0
    monthly_cost = defaultdict(float)
    yearly_cost = defaultdict(float)
    for r in records:
        if len(r) >= 3:
            try:
                amount = float(r[1])
                total_cost += amount
                dt = datetime.strptime(r[2], '%Y-%m-%d')
                year, month = dt.year, dt.month
                monthly_cost[(year, month)] += amount
                yearly_cost[year] += amount
            except (ValueError, IndexError):
                continue

    monthly_cost = OrderedDict(sorted(monthly_cost.items()))
    yearly_cost = OrderedDict(sorted(yearly_cost.items()))

    monthly_costs = list(monthly_cost.values())
    if len(monthly_costs) >= 3:
        predicted_next_month = sum(monthly_costs[-3:]) / 3
    elif monthly_costs:
        predicted_next_month = sum(monthly_costs) / len(monthly_costs)
    else:
        predicted_next_month = 0.0

    total = sum(monthly_costs)
    budget = read_budget()
    return render_template(
        'report.html',
        monthly=monthly_cost,
        yearly=yearly_cost,
        total=total,
        predicted_next_month=predicted_next_month,
        budget=budget
    )

@app.route('/report/pdf')
def report_pdf():
    user_email = session.get('user', 'Guest')
    records = read_records()
    total_cost = 0.0
    monthly_cost = defaultdict(float)
    yearly_cost = defaultdict(float)
    for r in records:
        if len(r) >= 3:
            try:
                amount = float(r[1])
                total_cost += amount
                dt = datetime.strptime(r[2], '%Y-%m-%d')
                year, month = dt.year, dt.month
                monthly_cost[(year, month)] += amount
                yearly_cost[year] += amount
            except (ValueError, IndexError):
                continue

    monthly_cost = OrderedDict(sorted(monthly_cost.items()))
    yearly_cost = OrderedDict(sorted(yearly_cost.items()))

    monthly_costs = list(monthly_cost.values())
    if len(monthly_costs) >= 3:
        predicted_next_month = sum(monthly_costs[-3:]) / 3
    elif monthly_costs:
        predicted_next_month = sum(monthly_costs) / len(monthly_costs)
    else:
        predicted_next_month = 0.0

    total = sum(monthly_costs)
    budget = read_budget()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph(f"Expense Report", styles['Title']))
    elements.append(Paragraph(f"User: {user_email}", styles['Normal']))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Monthly Table
    elements.append(Paragraph("Monthly Expenses", styles['Heading2']))
    data = [["Year", "Month", "Amount (ZAR)"]]
    for (y, m), amt in monthly_cost.items():
        data.append([str(y), str(m), f"R{amt:.2f}"])
    t = Table(data, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    # Yearly Table
    elements.append(Paragraph("Yearly Expenses", styles['Heading2']))
    data = [["Year", "Amount (ZAR)"]]
    for y, amt in yearly_cost.items():
        data.append([str(y), f"R{amt:.2f}"])
    t = Table(data, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    # Summary
    elements.append(Paragraph(f"Total Expenses: R{total:.2f}", styles['Normal']))
    elements.append(Paragraph(f"Predicted Next Month: R{predicted_next_month:.2f}", styles['Normal']))
    if budget is not None:
        elements.append(Paragraph(f"Budget: R{budget:.2f}", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="expense_report.pdf", mimetype='application/pdf')

@app.route('/exit')
def exit_app():
    return "Thank you! You can close the browser."

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname'].strip()
        cellphone = request.form['cellphone'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        confirm = request.form['confirm']
        users = get_users()
        if not fullname or not cellphone or not email or not password:
            flash("All fields are required.")
        elif password != confirm:
            flash("Passwords do not match.")
        elif email in users:
            flash("Email already registered.")
        else:
            with open('users.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([fullname, cellphone, email, password])
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        users = get_users()
        if email in users and users[email]['password'] == password:
            session['user'] = email
            flash("Login successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)