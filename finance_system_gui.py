import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt

# Database setup
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()

# Functions
def add_transaction(t_type):
    amount = entry_amount.get().strip()
    category = entry_category.get().strip()

    if amount == "" or category == "":
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    date = datetime.date.today().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)",
                   (t_type, amount, category, date))
    conn.commit()
    messagebox.showinfo("Success", f"{t_type} added successfully!")
    entry_amount.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    view_transactions()

def view_transactions():
    listbox_transactions.delete(0, tk.END)
    cursor.execute("SELECT type, amount, category, date FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()
    for row in rows:
        listbox_transactions.insert(tk.END, f"{row[0]} | ₹{row[1]} | {row[2]} | {row[3]}")

def show_summary():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expense = cursor.fetchone()[0] or 0
    savings = income - expense
    messagebox.showinfo("Summary", f"Income: ₹{income}\nExpense: ₹{expense}\nSavings: ₹{savings}")

def plot_expenses():
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    data = cursor.fetchall()
    if not data:
        messagebox.showinfo("No Data", "No expenses to plot!")
        return
    
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title("Expenses by Category")
    plt.show()

# GUI setup
root = tk.Tk()
root.title("Personal Finance System")
root.geometry("600x500")
root.config(bg="#f5f5f5")

# Amount & Category
tk.Label(root, text="Amount (₹):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_amount = tk.Entry(root, width=20)
entry_amount.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_category = tk.Entry(root, width=20)
entry_category.grid(row=1, column=1, padx=10, pady=10)

# Buttons
tk.Button(root, text="Add Income", command=lambda: add_transaction("Income"), bg="green", fg="white").grid(row=2, column=0, padx=10, pady=10)
tk.Button(root, text="Add Expense", command=lambda: add_transaction("Expense"), bg="red", fg="white").grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Show Summary", command=show_summary, bg="blue", fg="white").grid(row=2, column=2, padx=10, pady=10)
tk.Button(root, text="Plot Expenses", command=plot_expenses, bg="purple", fg="white").grid(row=2, column=3, padx=10, pady=10)

# Transactions list
listbox_transactions = tk.Listbox(root, width=70, height=15)
listbox_transactions.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

# Show transactions at startup
view_transactions()

root.mainloop()
