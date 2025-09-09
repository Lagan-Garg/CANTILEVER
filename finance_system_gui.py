import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("finance.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, category TEXT, amount REAL)")
conn.commit()

def add_expense():
    category = entry_category.get()
    amount = entry_amount.get()
    if category and amount:
        try:
            c.execute("INSERT INTO expenses (category, amount) VALUES (?, ?)", (category, float(amount)))
            conn.commit()
            messagebox.showinfo("Success", "Expense added successfully")
            entry_category.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Invalid amount")
    else:
        messagebox.showwarning("Error", "All fields are required")

def view_expenses():
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()
    if not rows:
        messagebox.showinfo("Expenses", "No records found")
    else:
        records = ""
        for row in rows:
            records += f"Category: {row[1]}, Amount: {row[2]}\n"
        messagebox.showinfo("Expenses", records)

def show_chart():
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = c.fetchall()
    if not data:
        messagebox.showinfo("Chart", "No data to display")
        return
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title("Expenses by Category")
    plt.show()

root = tk.Tk()
root.title("Personal Finance System")
root.geometry("400x300")

tk.Label(root, text="Category").pack()
entry_category = tk.Entry(root)
entry_category.pack()

tk.Label(root, text="Amount").pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="View Expenses", command=view_expenses).pack(pady=5)
tk.Button(root, text="Show Chart", command=show_chart).pack(pady=5)

root.mainloop()
