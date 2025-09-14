import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

class FinanceApp:
    def __init__(self, root):
        # Database setup
        self.conn = sqlite3.connect("finance_data.db")
        self.cur = self.conn.cursor()
        self.create_table_if_not_exists()

        # Window setup
        self.root = root
        self.root.title("Personal Finance System")
        self.root.geometry("600x400")

        # Main frame
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True)

        # Income input
        self.income_label = tk.Label(self.frame, text="Income:")
        self.income_label.grid(row=0, column=0, padx=5, pady=5)
        self.income_entry = tk.Entry(self.frame)
        self.income_entry.grid(row=0, column=1, padx=5, pady=5)

        # Expense input
        self.exp_label = tk.Label(self.frame, text="Expense:")
        self.exp_label.grid(row=1, column=0, padx=5, pady=5)
        self.exp_entry = tk.Entry(self.frame)
        self.exp_entry.grid(row=1, column=1, padx=5, pady=5)

        # Savings input
        self.save_label = tk.Label(self.frame, text="Savings:")
        self.save_label.grid(row=2, column=0, padx=5, pady=5)
        self.save_entry = tk.Entry(self.frame)
        self.save_entry.grid(row=2, column=1, padx=5, pady=5)

        # Action buttons (default colors)
        self.add_btn = tk.Button(self.frame, text="Add Entry", command=self.add_entry)
        self.add_btn.grid(row=3, column=0, pady=10)

        self.view_btn = tk.Button(self.frame, text="View Data", command=self.view_data)
        self.view_btn.grid(row=3, column=1, pady=10)

        self.plot_btn = tk.Button(self.frame, text="Show Chart", command=self.plot_data)
        self.plot_btn.grid(row=3, column=2, pady=10)

        self.delete_btn = tk.Button(self.frame, text="Delete Entry", command=self.delete_entry)
        self.delete_btn.grid(row=3, column=3, pady=10)

        # Data table
        self.tree = ttk.Treeview(
            self.frame,
            columns=("id", "income", "expense", "savings"),
            show="headings"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("income", text="Income")
        self.tree.heading("expense", text="Expense")
        self.tree.heading("savings", text="Savings")
        self.tree.column("id", width=50, stretch=tk.NO)
        self.tree.grid(row=4, column=0, columnspan=4, pady=20)

    def create_table_if_not_exists(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS finance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income REAL,
            expense REAL,
            savings REAL
        )
        """)
        self.conn.commit()

    def add_entry(self):
        try:
            inc = float(self.income_entry.get() or 0)
            exp = float(self.exp_entry.get() or 0)
            sav = float(self.save_entry.get() or 0)
            self.cur.execute(
                "INSERT INTO finance(income, expense, savings) VALUES (?, ?, ?)",
                (inc, exp, sav)
            )
            self.conn.commit()
            self.view_data()
            self.income_entry.delete(0, tk.END)
            self.exp_entry.delete(0, tk.END)
            self.save_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.cur.execute("SELECT id, income, expense, savings FROM finance")
        rows = self.cur.fetchall()
        for r in rows:
            self.tree.insert("", "end", values=r)

    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an entry to delete.")
            return

        item_data = self.tree.item(selected_item)
        record_id = item_data['values'][0]

        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this entry?")
        if response:
            try:
                self.cur.execute("DELETE FROM finance WHERE id = ?", (record_id,))
                self.conn.commit()
                self.tree.delete(selected_item)
                messagebox.showinfo("Success", "Entry deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def plot_data(self):
        self.cur.execute("SELECT SUM(income), SUM(expense), SUM(savings) FROM finance")
        vals = self.cur.fetchone()
        if vals and any(vals):
            cats = ["Income", "Expense", "Savings"]
            plt.bar(cats, vals, color=["green", "red", "blue"])
            plt.title("Finance Overview")
            plt.show()
        else:
            messagebox.showinfo("Info", "No data to plot.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
