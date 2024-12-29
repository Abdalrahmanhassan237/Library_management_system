
# Library Management System

![Library System Interface](https://github.com/user-attachments/assets/f451d766-c986-40d4-9dc4-e4cb698c146f)

## Introduction

This **Library Management System** is a comprehensive solution built with Python, featuring a modern graphical user interface (GUI) powered by `customtkinter`. The system provides complete library management capabilities including user authentication, member management, book tracking, and fine management, all backed by a robust MySQL database.

## Table of Contents
- [Features](#features)
- [System Components](#system-components)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

### Authentication & User Management
- Secure login system with bcrypt password hashing
- Role-based access control (admin, staff, member)
- "Remember Me" functionality
- Comprehensive user registration system
- Member information and contact management

### Book Management
- Complete book catalog system
- ISBN tracking
- Multiple authors support
- Genre categorization
- Availability status tracking

### Borrowing System
- Book checkout and return processing
- Due date management
- Fine calculation and tracking
- Active borrowing tracking
- Fine waiver system

## System Components

### Authentication Interface
- Login and registration forms
- Role-based access control
- User profile management
- Member contact information management

### Library Management Interface
- Book catalog management
- Borrowing processing
- Fine management
- Member management

## Prerequisites
- Python 3.x
- MySQL Server
- Required Python packages:
  ```bash
  pip install customtkinter pillow mysql-connector-python bcrypt
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/Abdalrahmanhassan237/Library_management_system/]
   ```

2. Install required packages:
   ```bash
   pip install customtkinter pillow mysql-connector-python bcrypt
   ```

3. Set up the MySQL database (see Database Schema section)

4. Configure the application

5. Run the application:
   ```bash
   python login_gui.py
   ```

## Database Schema

```sql
-- Create Library Database
CREATE DATABASE Library;
USE Library;

-- Users Table
CREATE TABLE Users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff', 'member') NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Books Table
CREATE TABLE Books (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    isbn VARCHAR(20) UNIQUE NOT NULL,
    publication_date DATE,
    availability_status VARCHAR(50) NOT NULL
);

-- Members Table
CREATE TABLE Members (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNIQUE,
    membership_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Borrowing Table
CREATE TABLE Borrowing (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    book_id BIGINT NOT NULL,
    member_id BIGINT NOT NULL,
    borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL,
    returned_at TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES Books(id),
    FOREIGN KEY (member_id) REFERENCES Members(id)
);

-- Index for Active Borrowings
CREATE INDEX idx_active_borrowing ON Borrowing(book_id, member_id, returned_at);

-- Fines Table
CREATE TABLE Fines (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    borrowing_id BIGINT UNIQUE,
    fine_amount DECIMAL(10, 2) NOT NULL,
    waived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (borrowing_id) REFERENCES Borrowing(id)
);

-- Book Authors Table
CREATE TABLE book_author (
    book_id BIGINT,
    author VARCHAR(255),
    PRIMARY KEY (book_id, author),
    FOREIGN KEY (book_id) REFERENCES Books(id)
);

-- Member Contact Information Table
CREATE TABLE Member_contact (
    member_id BIGINT,
    contact_info VARCHAR(255),
    PRIMARY KEY (member_id, contact_info),
    FOREIGN KEY (member_id) REFERENCES Members(id)
);
```

### Database Structure Overview
- **Users**: Stores user authentication and role information
- **Books**: Manages book catalog and availability
- **Members**: Tracks library member information
- **Borrowing**: Records book checkouts and returns
- **Fines**: Manages late return penalties
- **book_author**: Handles multiple authors per book
- **Member_contact**: Stores member contact information

## Configuration

### Database Connection
Update the database connection parameters:
```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="Library"
)
```

### User Roles
The system supports three user roles:
- **Admin**: Full system access and management
- **Staff**: Library operations and member management
- **Member**: Book browsing and borrowing capabilities

## Usage

### User Management
1. Register new users with appropriate roles
2. Manage member profiles and contact information
3. Track member borrowing history

### Book Management
1. Add new books with full details
2. Update book availability status
3. Manage multiple authors per book
4. Track book borrowing history

### Borrowing Process
1. Check out books to members
2. Set and track due dates
3. Process returns
4. Calculate and manage fines



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.


## Contributors

- **[Abdelrahman Hassan]** - Project Lead and Developer
