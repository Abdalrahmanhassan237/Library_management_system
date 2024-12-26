CREATE DATABASE Library;
USE Library;
CREATE TABLE Users (id BIGINT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(255) UNIQUE NOT NULL,
 password_hash VARCHAR(255) NOT NULL,
 role ENUM('admin', 'staff', 'member') NOT NULL,
 email VARCHAR(255) UNIQUE NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
 
CREATE TABLE Books (id BIGINT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(255) NOT NULL,
genre VARCHAR(100),
isbn VARCHAR(20) UNIQUE NOT NULL,
publication_date DATE,
availability_status VARCHAR(50) NOT NULL);

CREATE TABLE Members (id BIGINT AUTO_INCREMENT PRIMARY KEY,
user_id BIGINT UNIQUE,
membership_id VARCHAR(50) UNIQUE NOT NULL,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL,
 joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (user_id) REFERENCES Users(id));
 
CREATE TABLE Borrowing (id BIGINT AUTO_INCREMENT PRIMARY KEY,
book_id BIGINT NOT NULL,
member_id BIGINT NOT NULL, 
borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
due_date DATE NOT NULL,
returned_at TIMESTAMP,
FOREIGN KEY (book_id) REFERENCES Books(id),
FOREIGN KEY (member_id) REFERENCES Members(id));

-- Add an index to track active borrowings
CREATE INDEX idx_active_borrowing ON Borrowing(book_id, member_id, returned_at);

CREATE TABLE Fines (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
borrowing_id BIGINT UNIQUE,
fine_amount DECIMAL(10, 2) NOT NULL,
waived BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (borrowing_id) REFERENCES Borrowing(id));

CREATE TABLE book_author (
book_id BIGINT auto_increment, 
author VARCHAR(255) ,
primary key (book_id , author) , 
foreign key (book_id) references books(id)

);

CREATE TABLE Member_contact(
member_id BIGINT AUTO_INCREMENT , 
contact_info VARCHAR(255) ,

PRIMARY KEY (member_id , contact_info) ,
FOREIGN KEY  (member_id) REFERENCES Members(id)

);
