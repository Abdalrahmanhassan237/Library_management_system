from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk
import bcrypt
import mysql.connector

# Set appearance mode and default theme
set_appearance_mode("light")
set_default_color_theme("dark-blue")

# Create the main window
app = CTk()
app.geometry("950x750")
app.title("Signup Form")
app.resizable(0, 0)

# Set background image to the right side
pattern_image = ImageTk.PhotoImage(
    Image.open("./photos/bg_2.jpg").resize((580, 950))
)  # Adjust size as needed
image_label = CTkLabel(master=app, image=pattern_image, text="")
image_label.place(x=490, y=0)


def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="12345", database="library"
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


def register_user():
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    role = role_combobox.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    membership_id = membership_id_entry.get()

    # Validation
    if not username or not email or not password or not confirm_password or not role:
        messagebox.showwarning("Input Error", "All fields are required.")
        return
    if password != confirm_password:
        messagebox.showerror("Input Error", "Passwords do not match.")
        return
    if not first_name or not last_name or not membership_id:
        messagebox.showwarning("Input Error", "Personal details are required.")
        return

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )

    # Insert into the database
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Insert into Users table
            user_query = """
                INSERT INTO Users (username, password_hash, role, email)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(user_query, (username, password_hash, role, email))
            user_id = cursor.lastrowid  # Get the generated user ID

            # Insert into Members table
            member_query = """
                INSERT INTO Members (user_id, membership_id, first_name, last_name)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                member_query, (user_id, membership_id, first_name, last_name)
            )

            connection.commit()
            messagebox.showinfo("Success", "User registered successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            connection.close()


# Labels and Entry Fields
username_label = CTkLabel(app, text="Username", font=("Montserrat-Regular", 17))
username_label.place(x=27, y=30)
username_entry = CTkEntry(app, placeholder_text="Enter Username", width=430)
username_entry.place(x=27, y=70)

email_label = CTkLabel(app, text="Email", font=("Montserrat-Regular", 17))
email_label.place(x=27, y=110)
email_entry = CTkEntry(app, placeholder_text="Enter Email", width=430)
email_entry.place(x=27, y=150)

password_label = CTkLabel(app, text="Password", font=("Montserrat-Regular", 17))
password_label.place(x=27, y=190)
password_entry = CTkEntry(app, placeholder_text="Enter Password", width=430, show="*")
password_entry.place(x=27, y=230)

confirm_password_label = CTkLabel(
    app, text="Confirm Password", font=("Montserrat-Regular", 17)
)
confirm_password_label.place(x=27, y=270)
confirm_password_entry = CTkEntry(
    app, placeholder_text="Confirm Password", width=430, show="*"
)
confirm_password_entry.place(x=27, y=310)

role_label = CTkLabel(app, text="Role", font=("Montserrat-Regular", 17))
role_label.place(x=27, y=350)
role_combobox = CTkComboBox(app, values=["admin", "staff", "member"], width=430)
role_combobox.place(x=27, y=390)

first_name_label = CTkLabel(app, text="First Name", font=("Montserrat-Regular", 17))
first_name_label.place(x=27, y=430)
first_name_entry = CTkEntry(app, placeholder_text="Enter First Name", width=430)
first_name_entry.place(x=27, y=470)

last_name_label = CTkLabel(app, text="Last Name", font=("Montserrat-Regular", 17))
last_name_label.place(x=27, y=510)
last_name_entry = CTkEntry(app, placeholder_text="Enter Last Name", width=430)
last_name_entry.place(x=27, y=550)

membership_id_label = CTkLabel(
    app, text="Membership ID", font=("Montserrat-Regular", 17)
)
membership_id_label.place(x=27, y=590)
membership_id_entry = CTkEntry(app, placeholder_text="Enter Membership ID", width=430)
membership_id_entry.place(x=27, y=630)

# Register Button
register_button = CTkButton(app, text="Register", command=register_user, width=430)
register_button.place(x=27, y=680)

app.mainloop()
