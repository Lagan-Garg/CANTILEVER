import tkinter as tk
from tkinter import messagebox
import os

CONTACTS_FILE = "contacts.txt"

# Load contacts from file
def load_contacts():
    contacts = {}
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            for line in file:
                name, phone, email = line.strip().split("|")
                contacts[name] = {"phone": phone, "email": email}
    return contacts

# Save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        for name, info in contacts.items():
            file.write(f"{name}|{info['phone']}|{info['email']}\n")

# Add contact
def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()

    if name == "" or phone == "" or email == "":
        messagebox.showerror("Error", "All fields are required!")
        return
    
    contacts[name] = {"phone": phone, "email": email}
    save_contacts(contacts)
    messagebox.showinfo("Success", "Contact added successfully!")
    clear_entries()
    refresh_contacts()

# View all contacts
def refresh_contacts():
    listbox_contacts.delete(0, tk.END)
    for name, info in contacts.items():
        listbox_contacts.insert(tk.END, f"{name} | {info['phone']} | {info['email']}")

# Search contact
def search_contact():
    query = entry_search.get().strip()
    listbox_contacts.delete(0, tk.END)
    for name, info in contacts.items():
        if query.lower() in name.lower():
            listbox_contacts.insert(tk.END, f"{name} | {info['phone']} | {info['email']}")

# Delete contact
def delete_contact():
    selected = listbox_contacts.get(tk.ACTIVE)
    if not selected:
        messagebox.showerror("Error", "Please select a contact to delete!")
        return
    name = selected.split(" | ")[0]
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        messagebox.showinfo("Deleted", "Contact deleted successfully!")
        refresh_contacts()

# Clear input fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# ------------------- GUI -------------------
contacts = load_contacts()

root = tk.Tk()
root.title("Contact Book")
root.geometry("500x400")
root.config(bg="#f5f5f5")

# Labels & Entries
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Phone:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_phone = tk.Entry(root, width=30)
entry_phone.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=2, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Contact", command=add_contact, bg="green", fg="white").grid(row=3, column=0, padx=10, pady=10)
tk.Button(root, text="Delete Contact", command=delete_contact, bg="red", fg="white").grid(row=3, column=1, padx=10, pady=10)

# Search
tk.Label(root, text="Search:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_search = tk.Entry(root, width=30)
entry_search.grid(row=4, column=1, padx=10, pady=5)
tk.Button(root, text="Search", command=search_contact, bg="blue", fg="white").grid(row=4, column=2, padx=10, pady=5)

# Contact List
listbox_contacts = tk.Listbox(root, width=60, height=10)
listbox_contacts.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

refresh_contacts()

root.mainloop()
