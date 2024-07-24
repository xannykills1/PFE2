import customtkinter, tkinter
import sqlite3
import re
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import Canvas

fen2 = customtkinter.CTk()
fen2.geometry('1050x750')
fen2.title('Online Tutoring')
fen2.iconbitmap('icons\\logo.ico')
database = "database.db"

entry3 = None  # Define entry3 in the global scope


def post1():
    # Connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Get information from entry fields
    full_name = entry1.get()
    email = entry2.get()
    phone_number = entry3.get()  # Access entry3 from the global scope
    subject = entry4.get()

    # Check if any of the entry fields are empty
    if not all((full_name, email, phone_number, subject)):
        messagebox.showerror("Error", "Please fill in all fields")
        return

    # Validate email format
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        messagebox.showerror("Error", "Invalid email format")
        return

    # Check if email already exists in the database
    c.execute("SELECT email FROM tutors WHERE email=?", (email,))
    existing_email = c.fetchone()
    if existing_email:
        messagebox.showerror("Error", "Email already exists")
        return

    # Validate phone number format
    if not re.match(r'^\d{10}$', phone_number):
        messagebox.showerror("Error", "Phone number must be 10 digits")
        return

    # Insert information into the database
    c.execute("INSERT INTO tutors (full_name, email, phone_number, subject) VALUES (?, ?, ?, ?)",
              (full_name, email, phone_number, subject))

    # Commit changes and close connection
    conn.commit()
    conn.close()



def home():
    frame = customtkinter.CTkScrollableFrame(fen2, width=860, height=740)
    frame.place(x=170, y=0)

    # Adding labels inside the frame
    label1 = customtkinter.CTkLabel(frame, text="", font=('bold', 18),width=500, height=500)
    label1.pack(pady=10)
    label2 = customtkinter.CTkLabel(frame, text="", font=('bold', 18), width=500, height=500)
    label2.pack(pady=10)
    label3 = customtkinter.CTkLabel(frame, text="", font=('bold', 18), width=500, height=500)
    label3.pack(pady=10)
    label4 = customtkinter.CTkLabel(frame, text="", font=('bold', 18), width=500, height=500)
    label4.pack(pady=10)


    # Create a scrollable frame to display tutor information


    # Connect to the database
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Retrieve tutors from the database
    c.execute("SELECT full_name, email, phone_number, subject FROM tutors")
    tutors = c.fetchall()

    # Close connection
    conn.close()

    # Calculate the width of each column and initial y-position
    column_width = 280  # Divide the available width into three equal parts
    x_positions = [70 + i * column_width for i in range(3)]
    y_position = 20

    # Prepare the text for display
    for idx, tutor in enumerate(tutors):
        tutor_info = f"Name: {tutor[0]}\n"
        tutor_info += f"Email: {tutor[1]}\n"
        tutor_info += f"Phone Number: {tutor[2]}\n"
        tutor_info += f"Subject: {tutor[3]}\n\n"

        # Calculate the position for each tutor label
        x_position = x_positions[idx % 3]
        if idx % 3 == 0 and idx != 0:
            y_position += 150

        # Create a label for the tutor information
        tutor_label = customtkinter.CTkLabel(frame, text=tutor_info, font=('bold', 12))
        tutor_label.place(x=x_position, y=y_position)




def aboutus1():
    help_label1 = customtkinter.CTkLabel(fen2, text='', font=("Arial", 14), justify="left", height=750, width=880,
                                         bg_color='#242424')
    help_label1.place(x=170, y=0)
    text1 = """
    About Us

    Welcome to our online tutoring platform! We are dedicated to providing high-quality education and personalized
    learning experiences to students of all ages and backgrounds. Our mission is to empower students to achieve their academic 
    goals and unlock their full potential through interactive and engaging tutoring sessions.

    At our tutoring program, we understand that every student is unique, with individual learning styles and challenges.
    That's why we offer a diverse team of experienced tutors who are passionate about education and committed to 
    tailoring their approach to meet each student's specific needs.

    Our tutors are experts in their respective fields, whether it's mathematics, science, language arts, or test preparation.
     They undergo rigorous screening and training to ensure they possess the knowledge, skills, and dedication necessary
      to guide students towards success.

    We believe in the importance of fostering a supportive and encouraging learning environment where students feel 
    comfortable asking questions, making mistakes, and exploring new concepts. 
    Through personalized attention and constructive feedback, our tutors strive to instill 
    confidence in students and foster a love for learning that extends beyond the classroom.

    Whether you're struggling with a particular subject, preparing for exams,
    or simply looking to enhance your academic skills, our tutoring program is here to help you succeed. 
    Join us on your educational journey and discover the difference personalized tutoring can make!
           """
    bg1 = customtkinter.CTkLabel(fen2, text=text1, font=('bold', 16))
    bg1.place(x=170, y=150)



def logout():
    fen2.destroy()


def tutor():
    global entry1, entry2, entry3, entry4  # Define entry3 within the global scope
    bg2 = customtkinter.CTkLabel(fen2, text="", width=880, height=750)
    bg2.place(x=170, y=0)
    lab = customtkinter.CTkLabel(bg2, text="You are about to join as a tutor", font=('BOLD', 20))
    lab.place(x=300, y=0)

    entry1 = customtkinter.CTkEntry(bg2, placeholder_text='Full Name', width=300, height=38)
    entry1.place(x=200, y=200)
    entry2 = customtkinter.CTkEntry(bg2, placeholder_text='Email', width=300, height=38)
    entry2.place(x=200, y=270)
    entry3 = customtkinter.CTkEntry(bg2, placeholder_text='Phone Number', width=300, height=38)
    entry3.place(x=200, y=340)
    entry3.bind("<KeyRelease>", validate_input)
    entry4 = customtkinter.CTkEntry(bg2, placeholder_text='Subject', width=300, height=38)
    entry4.place(x=200, y=410)

    post = customtkinter.CTkButton(bg2, text='Publish', font=('BOLD', 20), command=post1)
    post.place(x=500, y=500)


def validate_input(event):
    global entry3  # Access entry3 from the global scope
    # Get the current content of the entry
    current_text = entry3.get()
    # Remove any non-numeric characters
    validated_text = re.sub(r'\D', '', current_text)
    # Update the entry with the validated content
    entry3.delete(0, 'end')
    entry3.insert(0, validated_text)


bg = customtkinter.CTkLabel(fen2, text="", width=170, height=750, fg_color='#1f1f1f')
bg.place(x=0, y=0)

home = customtkinter.CTkButton(bg, text="Home", font=('BOLD', 20), fg_color='#1f1f1f', command=home)
home.place(x=5, y=50)

aboutus = customtkinter.CTkButton(bg, text="About us", font=('BOLD', 20), fg_color='#1f1f1f', command=aboutus1)
aboutus.place(x=5, y=100)

tutor = customtkinter.CTkButton(bg, text="Be a Tutor", font=('BOLD', 20), fg_color='#1f1f1f', command=tutor)
tutor.place(x=5, y=150)

logout = customtkinter.CTkButton(bg, text="Log Out", font=('BOLD', 20), fg_color='#1f1f1f', command=logout)
logout.place(x=5, y=200)

settings = customtkinter.CTkButton(bg, text="Settings", font=('BOLD', 20), fg_color='#1f1f1f')
settings.place(x=5, y=700)


fen2.mainloop()
