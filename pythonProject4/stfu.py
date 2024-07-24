import sqlite3
import customtkinter
from PIL import Image
from tkinter import BooleanVar, messagebox
from cryptography.fernet import Fernet
import importlib.util

CONFIG_FILE = 'config.key'


def signup():
    try:
        spec = importlib.util.spec_from_file_location("file2", "file2.py")
        file2 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(file2)
        # Additional signup logic if needed
    except Exception as e:
        messagebox.showerror("Error", f"Failed to sign up: {e}")


def sign_in():
    email = loginentry.get()
    password = passwordentry.get()

    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Fetch user from the database
    c.execute("SELECT * FROM accounts WHERE email=? AND password=?", (email, password))
    user = c.fetchone()

    conn.close()

    if user:
        fen.destroy()
        import file3
        # Here you can proceed with your application logic after successful login
        if check1_var.get():  # If "Remember me" checkbox is checked
            save_credentials(email, password)
    else:
        messagebox.showerror("Login Failed", "Invalid email or password")


def save_credentials(email, password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_email = cipher_suite.encrypt(email.encode())
    encrypted_password = cipher_suite.encrypt(password.encode())
    with open(CONFIG_FILE, 'wb') as file:
        file.write(key + b'\n')
        file.write(encrypted_email + b'\n')
        file.write(encrypted_password)


def load_credentials():
    try:
        with open(CONFIG_FILE, 'rb') as file:
            key = file.readline().strip()
            encrypted_email = file.readline().strip()
            encrypted_password = file.readline().strip()
            cipher_suite = Fernet(key)
            email = cipher_suite.decrypt(encrypted_email).decode()
            password = cipher_suite.decrypt(encrypted_password).decode()
            return email, password
    except FileNotFoundError:
        return None, None


fen = customtkinter.CTk()
fen.title('Online Tutoring')
fen.geometry('520x520')
fen.iconbitmap('icons\\logo.ico')
logoic = customtkinter.CTkImage(dark_image=Image.open("icons/logo1.png"),
                                size=(130, 130))

logo1 = customtkinter.CTkLabel(fen, text='', image=logoic, bg_color='#242424')
logo1.place(x=190, y=70)
loginentry = customtkinter.CTkEntry(fen, height=40, width=350, placeholder_text='Email')
loginentry.place(x=90, y=230)

passwordentry = customtkinter.CTkEntry(fen, height=40, width=350, show='*', placeholder_text='Password')
passwordentry.place(x=90, y=290)

# Load saved credentials
email, password = load_credentials()
if email and password:
    loginentry.insert(0, email)
    passwordentry.insert(0, password)

# Set check button to always be checked
check1_var = BooleanVar(value=True)

check1 = customtkinter.CTkCheckBox(fen, text='Remember me', variable=check1_var)
check1.place(x=90, y=340)

btn1 = customtkinter.CTkButton(fen, text='Sign in', width=100, font=("Book Antiqua", 18), command=sign_in)
btn1.place(x=130, y=380)

ors = customtkinter.CTkLabel(fen, text="--- OR ---", bg_color='#242424', fg_color="#242424")
ors.place(x=244, y=380)

btn2 = customtkinter.CTkButton(fen, text='Sign up', width=100, font=("Book Antiqua", 15), fg_color='#242424',
                               hover_color='#242424', command=signup)
btn2.place(x=290, y=380)

fen.mainloop()
