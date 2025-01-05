# Library Management System 

![Library System Interface](https://github.com/user-attachments/assets/f451d766-c986-40d4-9dc4-e4cb698c146f)

## Introduction

This **Library Management System - Admin GUI** is a Python-based application designed for administrators to manage library operations efficiently. Built using `customtkinter` for a modern graphical user interface (GUI) and MySQL for database management, this system provides comprehensive tools for managing books, members, borrowing, fines, and more.

---

## Table of Contents
- [Features](#features)
- [System Components](#system-components)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributors](#contributors)

---

## Features

### Admin-Specific Features
- **Dashboard**: View real-time statistics such as total books, borrowed books, overdue books, and total members.
- **Books Management**:
  - **Add Book**: Add new books with details like title, authors, ISBN, publication date, genre, and status.
  - **Modify Book**: Update existing book details.
  - **Delete Book**: Remove a specific book from the library.
  - **Delete All Books**: Clear all books from the library (with confirmation).
  - **Search Books**: Search for books by title, author, or ISBN.
- **Member Functions**:
  - **Borrow Book**: Borrow books on behalf of members.
  - **Return Book**: Process book returns and calculate fines for overdue books.
  - **Renew Book**: Extend the due date for borrowed books.
  - **View Borrowed Books**: View a list of currently borrowed books.
  - **View Fines**: View and manage fines for overdue books.
- **Admin Panel**:
  - **Manage Users**: Manage user accounts and roles (admin, staff, member).
  - **View All Fines**: View all fines across the library.
  - **System Settings**: Configure system-wide settings.
  - **Backup Database**: Backup the library database.
  - **Generate Reports**: Generate reports on library activities.

### General Features
- **Overdue Books**: View a list of overdue books with details like due date, days overdue, and fine amount.
- **Fine Calculation**: Automatically calculates fines for overdue books at $3 per day.
- **Database Integration**: All data is stored and managed in a MySQL database.

---

## System Components

### Authentication Interface
- Role-based access control (admin, staff, member).
- Secure login system with bcrypt password hashing.

### Library Management Interface
- **Admin Interface**:
  - Dashboard with real-time statistics.
  - Comprehensive book management tools.
  - Member management and borrowing functions.
  - Fine management and reporting tools.
- **User Interface**:
  - Borrow, return, renew, and buy books.
  - View overdue books and fines.

---

## Prerequisites
- **Python 3.x**
- **MySQL Server**
- Required Python packages:
  ```bash
  pip install customtkinter mysql-connector-python bcrypt
  ```

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Abdalrahmanhassan237/Library_management_system.git
   cd Library_management_system
   ```

2. **Install Required Packages**:
   ```bash
   pip install customtkinter mysql-connector-python bcrypt
   ```

3. **Set Up MySQL Database**:
   - Create a database named `library`.
   - Run the following SQL script to create the necessary tables:
     ```sql
          CREATE TABLE Books (
          id BIGINT AUTO_INCREMENT PRIMARY KEY,
          title VARCHAR(255) NOT NULL,
          genre VARCHAR(100),
          isbn VARCHAR(20) UNIQUE NOT NULL,
          publication_date DATE,
          availability_status VARCHAR(50) NOT NULL
      );
      
      CREATE TABLE Members (
          id BIGINT AUTO_INCREMENT PRIMARY KEY,
          user_id BIGINT UNIQUE,
          membership_id VARCHAR(50) UNIQUE NOT NULL,
          first_name VARCHAR(100) NOT NULL,
          last_name VARCHAR(100) NOT NULL,
          joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (user_id)
          REFERENCES Users (id)
      );
       
      CREATE TABLE Borrowing (
          id BIGINT AUTO_INCREMENT PRIMARY KEY,
          book_id BIGINT NOT NULL,
          member_id BIGINT NOT NULL,
          borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          due_date DATE NOT NULL,
          returned_at TIMESTAMP,
          FOREIGN KEY (book_id)
          REFERENCES Books (id),
          FOREIGN KEY (member_id)
          REFERENCES Members (id)
      );
     
      CREATE TABLE Fines (
          id BIGINT AUTO_INCREMENT PRIMARY KEY,
          borrowing_id BIGINT UNIQUE,
          fine_amount DECIMAL(10 , 2 ) NOT NULL,
          waived BOOLEAN DEFAULT FALSE,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (borrowing_id)
          REFERENCES Borrowing (id)
      );
      
      CREATE TABLE book_author (
          book_id BIGINT AUTO_INCREMENT,
          author VARCHAR(255),
          PRIMARY KEY (book_id , author),
          FOREIGN KEY (book_id)
          REFERENCES books (id)
      );
      
      CREATE TABLE Member_contact (
          member_id BIGINT AUTO_INCREMENT,
          contact_info VARCHAR(255),
          PRIMARY KEY (member_id , contact_info),
          FOREIGN KEY (member_id)
          REFERENCES Members (id)
      );
     ```

4. **Configure Database Connection**:
   - Update the database connection details in the `setup_database` method in `library_gui_admin.py`:
     ```python
     self.connection = mysql.connector.connect(
         host="localhost", 
         user="user name", 
         password="your password", 
         database="library"
     )
     ```

5. **Run the Application**:
   ```bash
   python login.py
   ```

---

## Database Schema

### Tables Overview
- **Books**: Stores book details.
- **book_author**: Stores the relationship between books and authors.
- **Users**: Stores user login details.
- **Members**: Stores member details.
- **Borrowing**: Tracks book borrowing details.
- **Fines**: Tracks fines for overdue books.

---

## Configuration

### Database Connection
Update the database connection parameters in the `setup_database` method:
```python
self.connection = mysql.connector.connect(
    host="localhost",
    user="user name",
    password="your password",
    database="library"
)
```

### User Roles
The system supports two user roles:
- **Admin**: Full system access and management.
- **User**: Book browsing, borrowing, and returning capabilities.

---

## Usage

### Admin Features
- **Dashboard**: View real-time statistics about the library.
- **Books Management**:
  - Add, modify, delete, and search books.
  - Manage book availability and status.
- **Member Functions**:
  - Borrow, return, and renew books on behalf of members.
  - View borrowed books and fines.
- **Admin Panel**:
  - Manage users, view fines, configure system settings, backup the database, and generate reports.

### User Features
- **Borrow Book**: Borrow a book from the library with a specified return date.
- **Return Book**: Return a borrowed book, with automatic fine calculation for overdue returns.
- **Renew Book**: Extend the due date of a borrowed book (if no fines are pending).
- **Buy Book**: Purchase a book, marking it as "sold" in the system.
- **Search Books**: Search for available books by title, genre, or ISBN.

---

## Contributors

- **[Abdelrahman Hassan]** - Project Lead and Developer

