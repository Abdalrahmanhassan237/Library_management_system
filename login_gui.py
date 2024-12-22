from customtkinter import *
from PIL import Image
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import bcrypt
import os

from library_gui import LibrarySystem


# Create database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="library",
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None


# Authentication
def authenticate_user(username, password):
    connection = create_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        connection.close()
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user["password_hash"].encode("utf-8")
        ):
            return True, user["role"]
        else:
            return False, None
    except Error as e:
        messagebox.showerror("Database Error", f"Error querying database: {e}")
        return False, None


# "Remember Me" functionality
def save_remembered_username(username):
    with open("remember_me.txt", "w") as file:
        file.write(username)


def load_remembered_username():
    if os.path.exists("remember_me.txt"):
        with open("remember_me.txt", "r") as file:
            return file.read().strip()
    return ""


def clear_remembered_username():
    if os.path.exists("remember_me.txt"):
        os.remove("remember_me.txt")


# Login functionality
def login():
    username = username_entry.get()
    password = password_entry.get()
    remember_me = remember_me_var.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    is_authenticated, role = authenticate_user(username, password)

    if is_authenticated:
        if remember_me:
            save_remembered_username(username)
        else:
            clear_remembered_username()

        messagebox.showinfo(
            "Success", f"Welcome {role.capitalize()}! Login successful."
        )

        root.destroy()
        library_system = LibrarySystem(role, username)
        library_system.run()
    else:
        messagebox.showerror("Error", "Invalid username or password!")


# Register functionality
def display_register_form():
    root.destroy()
    import signup_gui


# GUI setup
set_appearance_mode("light")
set_default_color_theme("dark-blue")
root = CTk()
root.geometry("950x700")
root.title("Login Page")
root.resizable(0, 0)

frame = CTkFrame(root, fg_color="white")
frame.pack(fill="both", expand=True)

# Load and create background image using CTkImage
bg_image = Image.open("./photos/bg_2.jpg")
pattern_image = CTkImage(light_image=bg_image, dark_image=bg_image, size=(480, 710))
image_label = CTkLabel(master=root, image=pattern_image, text="")
image_label.place(relx=1.0, rely=0.5, anchor="e")

heading_label = CTkLabel(
    frame,
    text="Library Management System",
    bg_color="white",
    text_color="#222C43",
    font=("Verdana", 20, "bold"),
    width=90,
)
heading_label.place(x=85, y=80)

# Load and create user icon using CTkImage
user_icon = Image.open("./photos/profile.png")
user_image = CTkImage(light_image=user_icon, dark_image=user_icon, size=(110, 110))
user_icon_label = CTkLabel(master=frame, image=user_image, text="", bg_color="white")
user_icon_label.place(x=200, y=150)

username_entry = CTkEntry(
    master=frame,
    placeholder_text="\tEnter Your Username",
    width=250,
    height=40,
)
password_entry = CTkEntry(
    master=frame,
    placeholder_text="\tEnter Your Password",
    width=250,
    height=40,
    show="*",
)
username_entry.place(x=137, y=320)
password_entry.place(x=137, y=381)

remember_me_var = IntVar()
remember_me = CTkCheckBox(
    master=frame,
    text="Remember Me",
    variable=remember_me_var,
    width=150,
    height=30,
    border_width=2,
    fg_color="#134074",
    bg_color="white",
    hover_color="#555555",
    text_color="black",
    corner_radius=10,
    cursor="hand2",
)
remember_me.place(x=195, y=460)

remembered_username = load_remembered_username()
if remembered_username:
    username_entry.insert(0, remembered_username)
    remember_me_var.set(1)

CTkButton(
    frame,
    text="Login",
    fg_color="#3F4672",
    width=120,
    height=40,
    hover_color="#F1911D",
    cursor="hand2",
    command=login,
).place(x=192, y=500)

register_button = CTkButton(
    master=frame,
    text="Register",
    fg_color="#3F4672",
    width=120,
    height=40,
    hover_color="#F1911D",
    cursor="hand2",
    command=display_register_form,
)
register_button.place(x=192, y=550)

root.mainloop()
