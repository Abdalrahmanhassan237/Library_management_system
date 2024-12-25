
![image](https://github.com/user-attachments/assets/f451d766-c986-40d4-9dc4-e4cb698c146f)

# Library Management System - Login Interface

## Introduction

This is a **Library Management System** built using Python, featuring a graphical user interface (GUI) powered by the `customtkinter` library. The system connects to a MySQL database to authenticate users and provides role-based access for library members and staff. The application supports a **"Remember Me"** feature, allowing users to save their login credentials for easier access in future sessions.

The project leverages several libraries such as **MySQL Connector** for database interaction, **bcrypt** for password hashing, and **PIL (Pillow)** for image processing. The user interface is designed to be intuitive, with an easy-to-navigate login form and background imagery.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Example](#example)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

---

## Features

- **Database Integration**: Connects to a MySQL database to manage user authentication and data storage.
- **Authentication**: Uses bcrypt for securely hashing passwords and validating user credentials.
- **Role-based Access**: Supports multiple user roles, such as **Member** and **Staff**, for different access levels.
- **Remember Me**: Allows users to save their username locally for future logins.
- **User Interface**: Custom UI elements built with `customtkinter`, providing a modern, intuitive design.
- **Error Handling**: Displays user-friendly error messages when issues arise (e.g., invalid login credentials or database connectivity problems).

---

## Installation

Follow these steps to set up the project:

### 1. Install Python 3.x

Ensure that **Python 3.x** is installed on your system. You can download it from the official [Python website](https://www.python.org/downloads/).

### 2. Install Required Packages

Install the necessary Python libraries using `pip`:

```bash
pip install customtkinter pillow mysql-connector-python bcrypt
```

### 3. Set Up MySQL Database

Make sure you have a MySQL server running. You need to create a database and a table for storing user data. Here is an example SQL script to create the necessary table:

```sql
CREATE DATABASE library;

USE library;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('member', 'staff') NOT NULL
);
```

### 4. Configure Database Connection

Edit the database connection parameters in the script to match your MySQL setup. In the `create_connection()` function, adjust the `host`, `user`, `password`, and `database` variables.

```python
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="12345",  # Replace with your MySQL password
            database="library"  # Replace with your database name
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None
```

---

## Usage

After the installation and configuration are complete, you can run the program to launch the login interface:

### Running the Application

Execute the script from the command line:

```bash
python login_gui.py
```

### Features in the GUI:

- **Login**: Enter your **username** and **password**, then click **Login** to authenticate.
- **Remember Me**: If selected, your username will be saved to a file and automatically populated on subsequent visits.
- **Register**: Clicking the **Register** button redirects to a registration form (handled in `signup_gui.py`).

---

## Configuration

The main configuration for the application involves the MySQL database connection:

- **Database Credentials**: Ensure that the MySQL `username`, `password`, and `database` are correctly configured in the `create_connection()` function.
- **User Roles**: Users can be assigned either **"staff"** or **"member"** roles. These roles are checked upon login to provide appropriate access.

```python
def authenticate_user(username, password):
    connection = create_connection()
    if not connection:
        return False, None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        connection.close()
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            return True, user["role"]
        else:
            return False, None
    except Error as e:
        messagebox.showerror("Database Error", f"Error querying database: {e}")
        return False, None
```

---

## Dependencies

The following Python libraries are used in this project:

- **`customtkinter`**: A custom version of `tkinter` for more advanced, modern UI components.
- **`Pillow (PIL)`**: A powerful image manipulation library used to load and display background images and icons.
- **`mysql-connector-python`**: To establish a connection and interact with the MySQL database.
- **`bcrypt`**: For hashing passwords securely.
- **`tkinter`**: The built-in Python library for creating GUI applications.

You can install these dependencies using `pip`:

```bash
pip install customtkinter pillow mysql-connector-python bcrypt
```

---

## Example

### Workflow:

1. **Login Screen**: When the user opens the app, they are presented with a login screen.
2. **Authentication**: The user enters their username and password. If the credentials are valid, they are granted access based on their role (Staff or Member).
3. **"Remember Me"**: If checked, the username is saved for future logins, simplifying the process for the next session.
4. **Role-based Access**: Based on the role, the user will be directed to the appropriate section of the library system.

---

## Troubleshooting

- **Database Connection Issues**: If the error message "Database Error" is shown, ensure your MySQL server is running and the database credentials are correct.
- **Incorrect Login Credentials**: If the login fails, double-check that the username and password match what is stored in the `Users` table. Passwords are hashed using `bcrypt` and cannot be checked in plain text.
- **Missing User Data**: If you encounter a situation where the user is not found in the database, ensure that the user exists in the `Users` table and has the correct role assigned.

---

## Contributors

- **[Abdelrahman Hassan]** - Project Lead and Developer
