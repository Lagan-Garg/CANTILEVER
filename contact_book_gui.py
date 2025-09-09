import tkinter as tk
from tkinter import messagebox
import os

# file to store contacts
CONTACT_FILE = "contacts.txt"

# load contacts from file
def load_contacts():
    data = {}
    if os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    data[parts[0]] = {"phone": parts[1], "email": parts[2]}
    return data

# save contacts to file
def save_contacts():
    with open(CONTACT_FILE, "w") as f:
        for name, info in contacts.items():
            f.write(f"{name}|{info['phone']}|{info['email']}\n")

# add a contact
def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()

    if name == "" or phone == "" or email == "":
        messagebox.showerror("Error", "All fields must be filled")
        return

    contacts[name] = {"phone": phone, "email": email}
    save_contacts()
    messagebox.showinfo("Success", "Contact saved successfully!")
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    display_contacts()

# show all contacts
def display_contacts():
    listbox.delete(0, tk.END)
    for name, info in contacts.items():
        listbox.insert(tk.END, f"{name} | {info['phone']} | {info['email']}")

# search a contact
def search_contact():
    q = entry_search.get().strip().lower()
    listbox.delete(0, tk.END)
    for name, info in contacts.items():
        if q in name.lower():
            listbox.insert(tk.END, f"{name} | {info['phone']} | {info['email']}")

# delete a contact
def delete_contact():
    selected = listbox.get(tk.ACTIVE)
    if not selected:
        messagebox.showerror("Error", "Select a contact first")
        return
    name = selected.split(" | ")[0]
    if name in contacts:
        del contacts[name]
        save_contacts()
        messagebox.showinfo("Deleted", "Contact removed")
        display_contacts()

# main gui
root = tk.Tk()
root.title("Contact Book")
root.geometry("550x400")

contacts = load_contacts()

# name input
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

# phone input
tk.Label(root, text="Phone:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_phone = tk.Entry(root, width=30)
entry_phone.grid(row=1, column=1, padx=10, pady=5)

# email input
tk.Label(root, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=2, column=1, padx=10, pady=5)

# buttons
tk.Button(root, text="Add", command=add_contact, bg="green", fg="white").grid(row=3, column=0, padx=10, pady=10)
tk.Button(root, text="Delete", command=delete_contact, bg="red", fg="white").grid(row=3, column=1, padx=10, pady=10)

# search
tk.Label(root, text="Search:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_search = tk.Entry(root, width=30)
entry_search.grid(row=4, column=1, padx=10, pady=5)
tk.Button(root, text="Search", command=search_contact, bg="blue", fg="white").grid(row=4, column=2, padx=10, pady=5)

# listbox
listbox = tk.Listbox(root, width=70, height=12)
listbox.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

display_contacts()
root.mainloop()
