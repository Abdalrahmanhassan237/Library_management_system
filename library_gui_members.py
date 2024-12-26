from customtkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, timedelta
import bcrypt


class Library_System:
    def __init__(self, role, username):
        self.role = role
        self.username = username
        self.connection = None
        self.cursor = None
        self.setup_database()  # Setup database first
        self.setup_main_window()

    def setup_database(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost", user="root", password="12345", database="library"
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            raise SystemExit("Failed to connect to database")

    def setup_main_window(self):
        self.root = CTk()
        self.root.title("Library Management System")
        self.root.geometry("1200x800")

        # Create main frame
        self.main_frame = CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create header
        header = CTkLabel(
            self.main_frame,
            text=f"Welcome {self.username} ({self.role})",
            font=("Helvetica", 24, "bold"),
        )
        header.pack(pady=20)

        # Search bar
        self.search_frame = CTkFrame(self.main_frame)
        self.search_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = CTkEntry(
            self.search_frame, placeholder_text="Search books...", width=300
        )
        self.search_entry.pack(side="left", padx=5)

        CTkButton(self.search_frame, text="Search", command=self.search_books).pack(
            side="left", padx=5
        )

        # Setup interface based on role
        if self.role == "admin":
            self.setup_admin_interface()
        else:
            self.setup_user_interface()

    def setup_admin_interface(self):
        # Buttons frame
        button_frame = CTkFrame(self.main_frame)
        button_frame.pack(fill="x", padx=20, pady=10)

        CTkButton(
            button_frame, text="Add Book", command=self.show_add_book_dialog
        ).pack(side="left", padx=5)

        CTkButton(
            button_frame, text="Modify Book", command=self.modify_selected_book
        ).pack(side="left", padx=5)

        CTkButton(
            button_frame, text="Delete Book", command=self.delete_selected_book
        ).pack(side="left", padx=5)

        CTkButton(button_frame, text="Delete All", command=self.delete_all_books).pack(
            side="left", padx=5
        )

        self.setup_tree_view()

    def setup_user_interface(self):
        # Buttons frame
        button_frame = CTkFrame(self.main_frame)
        button_frame.pack(fill="x", padx=20, pady=10)

        CTkButton(button_frame, text="Borrow Book", command=self.borrow_book).pack(
            side="left", padx=5
        )

        CTkButton(button_frame, text="Buy Book", command=self.buy_book).pack(
            side="left", padx=5
        )

        # Add new buttons
        CTkButton(button_frame, text="Return Book", command=self.return_book).pack(
            side="left", padx=5
        )

        CTkButton(button_frame, text="Renew Book", command=self.renew_book).pack(
            side="left", padx=5
        )

        # CTkButton(
        #     button_frame, text="Overdue Books", command=self.show_overdue_books
        # ).pack(side="left", padx=5)

        self.setup_tree_view()

    def setup_tree_view(self):
        # Create frame for treeview
        tree_frame = CTkFrame(self.main_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create Treeview
        columns = ("ID", "Title", "Genre", "ISBN", "Publication Date", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack elements
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load initial data
        self.load_books()

    def load_books(self):
        try:
            self.cursor.execute("SELECT * FROM Books")
            books = self.cursor.fetchall()

            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert books
            for book in books:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        book["id"],
                        book["title"],
                        book["genre"],
                        book["isbn"],
                        book["publication_date"],
                        book["availability_status"],
                    ),
                )
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error loading books: {e}")

    def show_add_book_dialog(self):
        dialog = CTkToplevel(self.root)
        dialog.title("Add New Book")
        dialog.geometry("400x500")

        # Book details entries
        CTkLabel(dialog, text="Title:").pack(pady=5)
        title_entry = CTkEntry(dialog)
        title_entry.pack(pady=5)

        CTkLabel(dialog, text="Genre:").pack(pady=5)
        genre_entry = CTkEntry(dialog)
        genre_entry.pack(pady=5)

        CTkLabel(dialog, text="ISBN:").pack(pady=5)
        isbn_entry = CTkEntry(dialog)
        isbn_entry.pack(pady=5)

        CTkLabel(dialog, text="Publication Date (YYYY-MM-DD):").pack(pady=5)
        pub_date_entry = CTkEntry(dialog)
        pub_date_entry.pack(pady=5)

        CTkLabel(dialog, text="Author:").pack(pady=5)
        author_entry = CTkEntry(dialog)
        author_entry.pack(pady=5)

        def save_book():
            try:
                # Insert into Books table
                self.cursor.execute(
                    """
                    INSERT INTO Books (title, genre, isbn, publication_date, availability_status)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                    (
                        title_entry.get(),
                        genre_entry.get(),
                        isbn_entry.get(),
                        pub_date_entry.get(),
                        "available",
                    ),
                )

                book_id = self.cursor.lastrowid

                # Insert into book_author table
                self.cursor.execute(
                    """
                    INSERT INTO book_author (book_id, author)
                    VALUES (%s, %s)
                """,
                    (book_id, author_entry.get()),
                )

                self.connection.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                dialog.destroy()
                self.load_books()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add book: {e}")

        CTkButton(dialog, text="Save Book", command=save_book).pack(pady=20)

    def modify_selected_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to modify")
            return

        book_id = self.tree.item(selected[0])["values"][0]

        # Show modification dialog similar to add_book but pre-filled
        dialog = CTkToplevel(self.root)
        dialog.title("Modify Book")
        dialog.geometry("400x500")

        # Get current book data
        self.cursor.execute("SELECT * FROM Books WHERE id = %s", (book_id,))
        book = self.cursor.fetchone()

        # Create and pre-fill entries
        CTkLabel(dialog, text="Title:").pack(pady=5)
        title_entry = CTkEntry(dialog)
        title_entry.insert(0, book["title"])
        title_entry.pack(pady=5)

        CTkLabel(dialog, text="Genre:").pack(pady=5)
        genre_entry = CTkEntry(dialog)
        genre_entry.insert(0, book["genre"])
        genre_entry.pack(pady=5)

        def save_modifications():
            try:
                self.cursor.execute(
                    """
                    UPDATE Books
                    SET title = %s, genre = %s
                    WHERE id = %s
                """,
                    (title_entry.get(), genre_entry.get(), book_id),
                )

                self.connection.commit()
                messagebox.showinfo("Success", "Book modified successfully!")
                dialog.destroy()
                self.load_books()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to modify book: {e}")

        CTkButton(dialog, text="Save Changes", command=save_modifications).pack(pady=20)

    def delete_selected_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            book_id = self.tree.item(selected[0])["values"][0]
            try:
                # Delete from book_author first (due to foreign key constraint)
                self.cursor.execute(
                    "DELETE FROM book_author WHERE book_id = %s", (book_id,)
                )
                # Then delete from Books
                self.cursor.execute("DELETE FROM Books WHERE id = %s", (book_id,))
                self.connection.commit()

                messagebox.showinfo("Success", "Book deleted successfully!")
                self.load_books()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete book: {e}")

    def delete_all_books(self):
        if messagebox.askyesno(
            "Confirm",
            "Are you sure you want to delete ALL books? This cannot be undone!",
        ):
            try:
                # Delete from book_author first (due to foreign key constraint)
                self.cursor.execute("DELETE FROM book_author")
                # Then delete from Books
                self.cursor.execute("DELETE FROM Books")
                self.connection.commit()

                messagebox.showinfo("Success", "All books deleted successfully!")
                self.load_books()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete books: {e}")

    def search_books(self):
        search_term = self.search_entry.get()
        try:
            self.cursor.execute(
                """
                SELECT * FROM Books 
                WHERE title LIKE %s 
                OR genre LIKE %s 
                OR isbn LIKE %s
            """,
                (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"),
            )

            books = self.cursor.fetchall()

            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert matching books
            for book in books:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        book["id"],
                        book["title"],
                        book["genre"],
                        book["isbn"],
                        book["publication_date"],
                        book["availability_status"],
                    ),
                )

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to search books: {e}")

    def borrow_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to borrow")
            return

        book_id = self.tree.item(selected[0])["values"][0]

        # Debug print to check the actual status
        self.cursor.execute(
            "SELECT availability_status FROM Books WHERE id = %s", (book_id,)
        )
        result = self.cursor.fetchone()
        print(
            f"Debug - Book status: '{result['availability_status']}'"
        )  # Add this line to see the actual status

        # Check if book is available - use strip() to remove any whitespace
        status = result["availability_status"].strip() if result else None

        if status.lower() != "available":
            messagebox.showwarning(
                "Warning", f"This book is not available for borrowing. Status: {status}"
            )
            return

        # Show borrowing dialog
        dialog = CTkToplevel(self.root)
        dialog.title("Borrow Book")
        dialog.geometry("300x200")

        CTkLabel(dialog, text="Return Date (YYYY-MM-DD):").pack(pady=5)
        return_date_entry = CTkEntry(dialog)
        # Set default return date to 14 days from now
        default_return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        return_date_entry.insert(0, default_return_date)
        return_date_entry.pack(pady=5)

        def process_borrowing():
            try:
                # Get member_id for current user
                self.cursor.execute(
                    """
                    SELECT m.id FROM Members m
                    JOIN Users u ON m.user_id = u.id
                    WHERE u.username = %s
                """,
                    (self.username,),
                )
                member = self.cursor.fetchone()

                if not member:
                    messagebox.showerror("Error", "User is not registered as a member")
                    return

                # Insert borrowing record
                self.cursor.execute(
                    """
                    INSERT INTO Borrowing (book_id, member_id, due_date)
                    VALUES (%s, %s, %s)
                """,
                    (book_id, member["id"], return_date_entry.get()),
                )

                # Update book status
                self.cursor.execute(
                    """
                    UPDATE Books SET availability_status = 'borrowed'
                    WHERE id = %s
                """,
                    (book_id,),
                )

                self.connection.commit()
                messagebox.showinfo("Success", "Book borrowed successfully!")
                dialog.destroy()
                self.load_books()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to borrow book: {e}")

        CTkButton(dialog, text="Confirm Borrowing", command=process_borrowing).pack(
            pady=20
        )

    def buy_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to buy")
            return

        book_id = self.tree.item(selected[0])["values"][0]

        # Debug print to check the actual status
        self.cursor.execute(
            "SELECT title, availability_status FROM Books WHERE id = %s", (book_id,)
        )
        result = self.cursor.fetchone()
        print(f"Debug - Book status: '{result['availability_status']}'")  # Debug print

        # Check if book is available - use strip() to remove any whitespace
        status = result["availability_status"].strip() if result else None

        if status.lower() != "available":
            messagebox.showwarning(
                "Warning", f"This book is not available for purchase. Status: {status}"
            )
            return

        if messagebox.askyesno(
            "Confirm", f"Are you sure you want to buy '{result['title']}'?"
        ):
            try:
                # Get member_id for current user
                self.cursor.execute(
                    """
                    SELECT m.id FROM Members m
                    JOIN Users u ON m.user_id = u.id
                    WHERE u.username = %s
                """,
                    (self.username,),
                )
                member = self.cursor.fetchone()

                if not member:
                    messagebox.showerror("Error", "User is not registered as a member")
                    return

                # Update book status to 'sold'
                self.cursor.execute(
                    """
                    UPDATE Books 
                    SET availability_status = 'sold' 
                    WHERE id = %s
                """,
                    (book_id,),
                )

                self.connection.commit()
                messagebox.showinfo("Success", "Book purchased successfully!")
                self.load_books()  # Refresh the book list

            except mysql.connector.Error as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to process purchase: {e}")

    def run(self):
        """Start the main application loop"""
        self.root.mainloop()

    def cleanup(self):
        """Clean up database connections when the application closes"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def __del__(self):
        """Destructor to ensure database connections are properly closed"""
        self.cleanup()

    def return_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to return")
            return

        book_id = self.tree.item(selected[0])["values"][0]

        try:
            # Check if the book is borrowed by this user
            self.cursor.execute(
                """
                SELECT b.id, b.due_date, m.id as member_id 
                FROM Borrowing b
                JOIN Members m ON b.member_id = m.id
                JOIN Users u ON m.user_id = u.id
                WHERE b.book_id = %s 
                AND u.username = %s
                AND b.return_date IS NULL
            """,
                (book_id, self.username),
            )

            borrowing = self.cursor.fetchone()
            if not borrowing:
                messagebox.showwarning("Warning", "You haven't borrowed this book")
                return

            # Calculate fine if overdue
            due_date = datetime.strptime(str(borrowing["due_date"]), "%Y-%m-%d")
            today = datetime.now()
            fine = 0

            if today.date() > due_date.date():
                days_overdue = (today.date() - due_date.date()).days
                fine = days_overdue * 1  # $1 per day fine

            # Update book status and return date
            self.cursor.execute(
                """
                UPDATE Books SET availability_status = 'available'
                WHERE id = %s
            """,
                (book_id,),
            )

            self.cursor.execute(
                """
                UPDATE Borrowing 
                SET return_date = NOW()
                WHERE id = %s
            """,
                (borrowing["id"],),
            )

            self.connection.commit()

            if fine > 0:
                messagebox.showwarning("Fine Due", f"Late return fine: ${fine}")
            else:
                messagebox.showinfo("Success", "Book returned successfully!")

            self.load_books()

        except mysql.connector.Error as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"Failed to process return: {e}")

    def renew_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to renew")
            return

        book_id = self.tree.item(selected[0])["values"][0]

        try:
            # Check if the book is borrowed by this user
            self.cursor.execute(
                """
                SELECT b.id, b.due_date 
                FROM Borrowing b
                JOIN Members m ON b.member_id = m.id
                JOIN Users u ON m.user_id = u.id
                WHERE b.book_id = %s 
                AND u.username = %s
                AND b.returned_at IS NULL
            """,
                (book_id, self.username),
            )

            borrowing = self.cursor.fetchone()
            if not borrowing:
                messagebox.showwarning("Warning", "You haven't borrowed this book")
                return

            # Check if there are any unpaid fines
            self.cursor.execute(
                """
                SELECT SUM(fine_amount) as total_fines
                FROM Fines
                WHERE borrowing_id = %s AND waived = FALSE
            """,
                (borrowing["id"],),
            )

            fines = self.cursor.fetchone()
            if fines and fines["total_fines"]:
                messagebox.showwarning(
                    "Warning", "Please pay your outstanding fines before renewing"
                )
                return

            # Extend due date by 14 days
            new_due_date = datetime.strptime(
                str(borrowing["due_date"]), "%Y-%m-%d"
            ) + timedelta(days=14)

            self.cursor.execute(
                """
                UPDATE Borrowing 
                SET due_date = %s
                WHERE id = %s
            """,
                (new_due_date.strftime("%Y-%m-%d"), borrowing["id"]),
            )

            self.connection.commit()
            messagebox.showinfo(
                "Success",
                f"Book renewed successfully! New due date: {new_due_date.strftime('%Y-%m-%d')}",
            )

        except mysql.connector.Error as e:
            self.connection.rollback()
            messagebox.showerror("Error", f"Failed to renew book: {e}")

    def show_overdue_books(self):
        # Create a new window for overdue books
        overdue_window = CTkToplevel(self.root)
        overdue_window.title("Overdue Books")
        overdue_window.geometry("800x600")

        # Create Treeview for overdue books
        tree_frame = CTkFrame(overdue_window)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("Title", "Due Date", "Days Overdue", "Fine Amount", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        try:
            # Get overdue books for the current user
            self.cursor.execute(
                """
                SELECT 
                    b.title, 
                    br.due_date,
                    COALESCE(f.fine_amount, 0) as fine_amount,
                    CASE 
                        WHEN f.waived = TRUE THEN 'Waived'
                        WHEN f.fine_amount IS NOT NULL THEN 'Pending Payment'
                        ELSE 'No Fine'
                    END as fine_status
                FROM Borrowing br
                JOIN Books b ON br.book_id = b.id
                JOIN Members m ON br.member_id = m.id
                JOIN Users u ON m.user_id = u.id
                LEFT JOIN Fines f ON br.id = f.borrowing_id
                WHERE u.username = %s
                AND br.returned_at IS NULL
                AND br.due_date < CURDATE()
            """,
                (self.username,),
            )

            overdue_books = self.cursor.fetchall()

            for book in overdue_books:
                due_date = datetime.strptime(str(book["due_date"]), "%Y-%m-%d")
                days_overdue = (datetime.now().date() - due_date.date()).days

                tree.insert(
                    "",
                    "end",
                    values=(
                        book["title"],
                        book["due_date"],
                        days_overdue,
                        f"${book['fine_amount']}" if book["fine_amount"] else "$0",
                        book["fine_status"],
                    ),
                )

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to load overdue books: {e}")

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


# Main execution
if __name__ == "__main__":
    # For testing purposes
    app = Library_System(role="user", username="test_user")
    try:
        app.run()
    finally:
        app.cleanup()
