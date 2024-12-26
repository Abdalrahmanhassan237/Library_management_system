USE library;

START TRANSACTION ;

# books data 
INSERT INTO Books (title, genre, isbn, publication_date, availability_status)
VALUES
('To Kill a Mockingbird', 'Fiction', '97800161120084', '1960-07-11', 'Available'),
('1984', 'Dystopian', '97804521524935', '1949-06-08', 'Available'),
('Moby Dick', 'Adventure', '9781853260087', '1851-10-18', 'Available'),
('The Great Gatsby', 'Classics', '9780743273565', '1925-04-10', 'Checked Out'),
('Pride and Prejudice', 'Romance', '9780141439518', '1813-01-28', 'Available'),
('The Catcher in the Rye', 'Fiction', '9780316769488', '1951-07-16', 'Available'),
('The Hobbit', 'Fantasy', '9780261103344', '1937-09-21', 'Checked Out'),
('War and Peace', 'Historical Fiction', '9781400079988', '1869-01-01', 'Available'),
('The Odyssey', 'Epic', '9780140268867', '0800-1-1', 'Available'),
('Crime and Punishment', 'Psychological Fiction', '9780486415871', '1866-01-01', 'Checked Out');

# users data 

INSERT INTO Users (username, password_hash, role, email) VALUES
('hazem', SHA2('hazem_123', 256), 'admin', 'admin@library.com'),
('ahmed123', SHA2('1209kjun', 256), 'staff', 'staff@library.com'),
('nour', SHA2('member_password1', 256), 'member', 'member1@library.com'),
('salma_123', SHA2('member_password2', 256), 'member', 'member2@library.com');

select * 
from books ;


SHOW TABLE STATUS LIKE 'Books';


select *
from borrowing ;

select * 
from users ;

select * 
from members ;

select * 
from fines;


# some fines data o test

INSERT INTO Fines (borrowing_id, fine_amount, waived) VALUES
(1, 15.00, FALSE),
(2, 10.00, TRUE),
(3, 20.50, FALSE),
(4, 5.00, FALSE);




