import tkinter as tk
from tkinter import messagebox, ttk
import os

FILE_NAME = "contacts.txt"

def load_data_file():
  contact_data = {}
  try:
    with open(FILE_NAME, "r") as file:
        for line in file:
          try:
            name, phone, email = line.strip().split(" | ")
            contact_data[name] = {"phone": phone, "email": email}
          except:
              pass
  except FileNotFoundError:
    pass
  return contact_data

def save_data_to_file(temp_contacts):
  with open(FILE_NAME, "w") as f:
    for aName, some_details in temp_contacts.items():
      f.write(aName + " | " + some_details['phone'] + " | " + some_details['email'] + "\n")

class My_App:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("My Awesome Contact App")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=6)
        style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))

        self.the_contacts = load_data_file()
        self.selected_contact = None  # Track currently selected contact

        temp_frame = ttk.Frame(root_window, padding="15 15 15 15")
        temp_frame.pack(fill=tk.BOTH, expand=True)

        titl_label = ttk.Label(temp_frame, text="My Contact Book", style='Header.TLabel')
        titl_label.grid(row=0, column=0, columnspan=3, pady=10)

        inpt_frame = ttk.LabelFrame(temp_frame, text="Contact Details", padding="10 10 10 10")
        inpt_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Configure column weights for proper expansion
        inpt_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(inpt_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(inpt_frame, width=40)
        self.name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Label(inpt_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.phoneEntry = ttk.Entry(inpt_frame, width=40)
        self.phoneEntry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Label(inpt_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(inpt_frame, width=40)
        self.email_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        button_frame = ttk.Frame(temp_frame, padding="10 0 10 0")
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)

        add_btn = ttk.Button(button_frame, text="Add Contact", command=self.add_contact)
        add_btn.grid(row=0, column=0, padx=5, pady=5)

        update_btn = ttk.Button(button_frame, text="Update Contact", command=self.updateContact)
        update_btn.grid(row=0, column=1, padx=5, pady=5)

        delete_btn = ttk.Button(button_frame, text="Delete Contact", command=self.delete_contact_by_name)
        delete_btn.grid(row=0, column=2, padx=5, pady=5)

        clear_btn = ttk.Button(button_frame, text="Clear Fields", command=self.clear_entries)
        clear_btn.grid(row=0, column=3, padx=5, pady=5)

        list_frame = ttk.LabelFrame(temp_frame, text="All Contacts", padding="10 10 10 10")
        list_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Configure grid weights for proper expansion
        temp_frame.grid_rowconfigure(3, weight=1)
        temp_frame.grid_columnconfigure(0, weight=1)
        temp_frame.grid_columnconfigure(1, weight=1)
        temp_frame.grid_columnconfigure(2, weight=1)

        self.scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.contacts_listbox = tk.Listbox(list_frame, width=70, height=12,
                                           yscrollcommand=self.scrollbar.set,
                                           font=('Helvetica', 10))
        self.scrollbar.config(command=self.contacts_listbox.yview)

        self.contacts_listbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        self.contacts_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.refresh_listbox_data()

    def refresh_listbox_data(self):
        self.contacts_listbox.delete(0, tk.END)
        temp_list = list(self.the_contacts.keys())
        temp_list.sort()

        for a_name in temp_list:
            self.contacts_listbox.insert(tk.END, a_name)

    def clear_entries(self):
        # Ensure name entry is editable before clearing
        self.name_entry.config(state=tk.NORMAL)
        self.name_entry.delete(0, tk.END)
        self.phoneEntry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.contacts_listbox.selection_clear(0, tk.END)
        # Store the current selection for update/delete operations
        self.selected_contact = None

    def on_listbox_select(self, event):
        i = self.contacts_listbox.curselection()
        if i:
            selected_name = self.contacts_listbox.get(i[0])
            details = self.the_contacts.get(selected_name)

            if details:  # Check if contact details exist
                # Clear entries but don't clear selection
                self.name_entry.config(state=tk.NORMAL)
                self.name_entry.delete(0, tk.END)
                self.phoneEntry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)

                # Store selected contact for operations
                self.selected_contact = selected_name

                # Populate fields
                self.name_entry.insert(0, selected_name)
                self.name_entry.config(state='readonly')
                self.phoneEntry.insert(0, details['phone'])
                self.email_entry.insert(0, details['email'])

    def add_contact(self):
        temp = self.name_entry.get()
        name = temp.strip()
        ph = self.phoneEntry.get()
        phone = ph.strip()
        mail = self.email_entry.get().strip()

        if len(name) == 0 or len(phone) == 0:
            messagebox.showerror("Error", "You need a name and phone number for the contact!")
            return

        for key_name in self.the_contacts:
            if key_name == name:
                messagebox.showerror("Error", "That name already exists. Pick another one.")
                return

        some_dict = {"phone": phone, "email": mail}
        self.the_contacts[name] = some_dict
        save_data_to_file(self.the_contacts)
        self.refresh_listbox_data()
        self.clear_entries()
        print("Contact added: " + name)
        messagebox.showinfo("Success", "Contact added successfully!")

    def updateContact(self):
        # Check if we have a selected contact stored
        if not hasattr(self, 'selected_contact') or not self.selected_contact:
            messagebox.showerror("Error", "Please select a contact from the list to update.")
            return

        # Check if the contact still exists in our data
        if self.selected_contact not in self.the_contacts:
            messagebox.showerror("Error", "Selected contact no longer exists.")
            self.clear_entries()
            return

        new_phone = self.phoneEntry.get().strip()
        new_email = self.email_entry.get().strip()

        if not new_phone:
            messagebox.showerror("Error", "Phone number cannot be empty!")
            self.phoneEntry.focus()
            return

        # Update the contact
        self.the_contacts[self.selected_contact]['phone'] = new_phone
        self.the_contacts[self.selected_contact]['email'] = new_email

        save_data_to_file(self.the_contacts)
        self.refresh_listbox_data()
        self.clear_entries()
        messagebox.showinfo("Success", f"Contact '{self.selected_contact}' updated successfully!")

    def delete_contact_by_name(self):
        # Check if we have a selected contact stored
        if not hasattr(self, 'selected_contact') or not self.selected_contact:
            messagebox.showerror("Error", "Please select a contact from the list to delete.")
            return

        # Check if the contact still exists in our data
        if self.selected_contact not in self.the_contacts:
            messagebox.showerror("Error", "Selected contact no longer exists.")
            self.clear_entries()
            return

        name_to_delete = self.selected_contact

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name_to_delete}'?\n\nThis action cannot be undone."):
            del self.the_contacts[name_to_delete]
            save_data_to_file(self.the_contacts)
            self.refresh_listbox_data()
            self.clear_entries()
            messagebox.showinfo("Success", f"Contact '{name_to_delete}' deleted successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = My_App(root)
    root.mainloop()
