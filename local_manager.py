import tkinter as tk
from tkinter import messagebox

import json
import random
import string
import os

print("Working directory:", os.getcwd())

# Set the file name for storing saved passwords
DATA_FILE = "data.json"
# Password generator function
def generate_password():
    # Combine all possible characters: letters a-z A-Z, digits 0-9 and symbols
    characters = string.ascii_letters + string.digits + string.punctuation
    # Randomly pick 16 characters from the character set
    password = ''.join(random.choice(characters) for _ in range(16))
    # Clear the password entry field first
    password_entry.delete(0, tk.END)
    # Insert the generated password into the entry field
    password_entry.insert(0, password)
# Save password function
def save_password():
    # Get text from input fields
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    # If any fields are empty warn user
    if not website or not username or not password:
        messagebox.showwarning("Oops.", "Please don't leave any fields empty.")
        return
    # Create a dictionary with the new entry
    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }
    
    data = {} # Hold existing data
    # If the data file exists, try to load it
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file) # Load existing data from json
        except json.JSONDecodeError:
            print("Existing file is empty or corrupted. Starting fresh.")
        
        # Update existing data with the new website entry
        data.update(new_data)
        # Save the update data back to the file
        try:
            with open(DATA_FILE, "w") as file:
                json.dump(data, file, indent=4) # Write file with formatting
            print(f"Saved: {new_data}")
            messagebox.showinfo("Succes", f"Credentals for '{website}' saved.")
        except Exception as e:
            print(f"Error saving file: {e}")
            # If something goes wrong show error message
            messagebox.showerror("Error", f"Failed to save: {e}")
            return
        # Clear the website and password fields after saving
        website_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        
def find_password():
    # Get the website name the user wants to search for
    website = website_entry.get()
    # If no file exists yet there"s nothing to search
    if not os.path.exists(DATA_FILE):
        messagebox.showerror("Error", "No data file found.")
        return
    # Try to open and read the json file
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file) # Load all saved data
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error reading the data file.")
        return
    # Check if the website is in the data
    if website in data:
        username = data[website]["username"]
        password = data[website]["password"]
        # Show the credentials in a popup
        messagebox.showinfo(website, f"Username: {username}\nPassword: {password}")
    else:
        # Inform the user that the website was not found
        messagebox.showinfo("Not Found", f"No details for '{website}' found.")
# GUI setup
# Create the main application window
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
# Label describe each input field
tk.Label(text="Website:").grid(row=0, column=0)
tk.Label(text="Username/Email:").grid(row=1, column=0)
tk.Label(text="Password:").grid(row=2, column=0)
# Entry field for website
website_entry = tk.Entry(width=35)
website_entry.grid(row=0, column=1, columnspan=2) # Span across 2 columns
website_entry.focus() # Auto focus on this field when the app starts
# Entry field for username/email
username_entry = tk.Entry(width=35)
username_entry.grid(row=1, column=1, columnspan=2)
# Entry field for password
password_entry = tk.Entry(width=21)
password_entry.grid(row=2, column=1)
# Button to search for a website's credentials
search_button = tk.Button(text="Search", width=13, command=find_password)
search_button.grid(row=0, column=3)
# Button to generate a random password
generate_button = tk.Button(text="Generate Password", command=generate_password)
generate_button.grid(row=2, column=2)
# Button to save the current entry to the json file
add_button = tk.Button(text="Add", width=36, command=save_password)
add_button.grid(row=3, column=1, columnspan=2)
# Run the GUI event loop (keeps window open)
window.mainloop() 
