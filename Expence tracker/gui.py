import tkinter as tk
from tkinter import ttk, messagebox
from expenses import Expense
import csv
import datetime
import calendar

expense_file_path = "expenses.csv"
budget = 5000

def save_expense_to_file(expense: Expense):
    with open(expense_file_path, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([expense.name, expense.amount, expense.category])

def summarize_expenses():
    expenses = []
    with open(expense_file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                expense_name, expense_amount, expense_category = row
                expenses.append(Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category,
                ))
    
    amount_by_category = {}
    for expense in expenses:
        if expense.category in amount_by_category:
            amount_by_category[expense.category] += expense.amount
        else:
            amount_by_category[expense.category] = expense.amount
    
    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = budget - total_spent
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_budget = remaining_budget / remaining_days if remaining_days else 0
    
    return {
        'expenses': amount_by_category,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'remaining_days': remaining_days,
        'daily_budget': daily_budget
    }

def add_expense():
    name = name_var.get()
    amount = float(amount_var.get())
    category = category_var.get()
    
    expense = Expense(name=name, category=category, amount=amount)
    save_expense_to_file(expense)
    result = summarize_expenses()
    update_summary(result)

def update_summary(result):
    expense_summary.delete(1.0, tk.END)
    expense_summary.insert(tk.END, f"Total Spent: ${result['total_spent']:.2f}\n")
    expense_summary.insert(tk.END, f"Remaining Budget: ${result['remaining_budget']:.2f}\n")
    expense_summary.insert(tk.END, f"Remaining Days: {result['remaining_days']}\n")
    expense_summary.insert(tk.END, f"Daily Budget: ${result['daily_budget']:.2f}\n\n")
    
    expense_summary.insert(tk.END, "Expenses by Category:\n")
    for category, amount in result['expenses'].items():
        expense_summary.insert(tk.END, f"{category}: ${amount:.2f}\n")

root = tk.Tk()
root.title("Expense Tracker")

name_var = tk.StringVar()
amount_var = tk.StringVar()
category_var = tk.StringVar()

tk.Label(root, text="Expense Name:").grid(row=0, column=0)
tk.Entry(root, textvariable=name_var).grid(row=0, column=1)

tk.Label(root, text="Amount:").grid(row=1, column=0)
tk.Entry(root, textvariable=amount_var).grid(row=1, column=1)

tk.Label(root, text="Category:").grid(row=2, column=0)
category_menu = ttk.Combobox(root, textvariable=category_var)
category_menu['values'] = ("food", "Home & Bills", "Work", "Fun", "travel", "others")
category_menu.grid(row=2, column=1)

tk.Button(root, text="Add Expense", command=add_expense).grid(row=3, columnspan=2)

expense_summary = tk.Text(root, width=40, height=10)
expense_summary.grid(row=4, columnspan=2)

root.mainloop()
