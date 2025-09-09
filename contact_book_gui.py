import tkinter as tk
from tkinter import messagebox
import os

def add_contact():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()
    if name and phone:
        with open("contacts.txt", "a") as f:
            f.write(f"{name},{phone},{email},{address}\n")
        messagebox.showinfo("Success", "Contact added successfully")
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_address.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Name and Phone are required")

def view_contacts():
    if not os.path.exists("contacts.txt"):
        messagebox.showinfo("Contacts", "No contacts found")
        return
    with open("contacts.txt", "r") as f:
        data = f.readlines()
    if not data:
        messagebox.showinfo("Contacts", "No contacts found")
    else:
        contacts = ""
        for line in data:
            name, phone, email, address = line.strip().split(",")
            contacts += f"Name: {name}, Phone: {phone}, Email: {email}, Address: {address}\n"
        messagebox.showinfo("Contacts", contacts)

root = tk.Tk()
root.title("Contact Book")
root.geometry("400x400")

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Phone").pack()
entry_phone = tk.Entry(root)
entry_phone.pack()

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root)
entry_email.pack()

tk.Label(root, text="Address").pack()
entry_address = tk.Entry(root)
entry_address.pack()

tk.Button(root, text="Add Contact", command=add_contact).pack(pady=5)
tk.Button(root, text="View Contacts", command=view_contacts).pack(pady=5)

root.mainloop()
