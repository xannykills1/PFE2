import customtkinter
import re
import sqlite3
import hashlib
from tkinter import *
from PIL import Image

# Set the appearance mode before creating the window
customtkinter.set_appearance_mode("dark")

# Function to create a new database table for accounts if it doesn't exist
def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts
                 (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, username TEXT, email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

# Function to register a new account
def register_account(first_name, last_name, username, email, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if the email already exists in the database
    c.execute("SELECT * FROM accounts WHERE email=?", (email,))
    existing_user = c.fetchone()

    if existing_user:
        # If the email already exists, display an error message
        error_label.config(text="Email already exists", fg="red", font=("Bold", 15))
    else:
        # Insert the new account into the database
        c.execute(
            "INSERT INTO accounts (first_name, last_name, username, email, password) VALUES (?, ?, ?, ?, ?)",
            (first_name, last_name, username, email, password))
        conn.commit()
        conn.close()

        # After successful signup, you may want to perform further actions or close the window
        # Here, we destroy all widgets to clear the window
        for widget in fen1.winfo_children():
            widget.destroy()
        # Optionally, display a message or perform other actions after signup
        success_label = Label(fen1, text="Signup successful!", fg="green", bg='#242424', font=("Bold", 20))
        success_label.pack()
        success_labels = Label(fen1, text="This window will be closed after 2 seconds", fg="green",
                               bg='#242424', font=("Bold", 10))
        success_labels.pack()
        fen1.after(2000, fen1.destroy)

def validate_email(email):
    # Regular expression for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def signup():
    # Retrieve user input from the entry widgets
    first_name = fn.get()
    last_name = ln.get()
    username = un.get()
    email_address = email.get()
    password = password_entry.get()

    # Perform basic validation
    if not (first_name and last_name and username and email_address and password):
        # If any field is empty, show an error message
        error_label.config(text="Please fill in all fields", fg="red", font=("BOLD", 15))
    elif password != confirm_password_entry.get():
        # If passwords don't match, show an error message
        error_label.config(text="Passwords do not match", fg="red", font=("BOLD", 15))
    elif not validate_email(email_address):
        # If email is not valid, show an error message
        error_label.config(text="Invalid email format", fg="red", font=("Bold", 15))
    else:
        # Perform signup actions here, such as saving data to a database
        register_account(first_name, last_name, username, email_address, password)


create_table()

fen1 = customtkinter.CTk()
fen1.title('Tsuki Medicine')
fen1.geometry('450x520')
fen1.resizable(width=False, height=False)

fn = customtkinter.CTkEntry(fen1, height=40, width=150, placeholder_text='First Name')
fn.place(x=60, y=100)

ln = customtkinter.CTkEntry(fen1, height=40, width=150, placeholder_text='Last Name')
ln.place(x=250, y=100)

un = customtkinter.CTkEntry(fen1, height=40, width=340, placeholder_text='Username')
un.place(x=60, y=170)

email = customtkinter.CTkEntry(fen1, height=40, width=340, placeholder_text='Email')
email.place(x=60, y=230)

password_entry = customtkinter.CTkEntry(fen1, height=40, width=340, show='*', placeholder_text='Password')
password_entry.place(x=60, y=290)

confirm_password_entry = customtkinter.CTkEntry(fen1, height=40, width=340, show='*', placeholder_text='Confirm Password')
confirm_password_entry.place(x=60, y=350)

btn1 = customtkinter.CTkButton(fen1, text='Sign up', width=100, font=("Book Antiqua", 20), command=signup)
btn1.place(x=180, y=420)

error_label = Label(fen1, text="", fg="red", bg='#242424', font=("BOLD", 20))
error_label.place(x=140, y=470)



fen1.mainloop()
