from customtkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, timedelta
import bcrypt


class LibrarySystem:
    def __init__(self, role, username):
        self.role = role
        self.username = username
        self.connection = None
        self.cursor = None
        self.current_frame = None  # Track current frame for back navigation
        self.frame_history = []  # Track frame history for back button
        self.setup_database()
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
        self.root.geometry("1400x800")

        # Create main container
        self.main_container = CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True)

        if self.role == "admin":
            # Create navigation frame (left sidebar) only for admin
            self.nav_frame = CTkFrame(self.main_container, width=200)
            self.nav_frame.pack(side="left", fill="y", padx=10, pady=10)
            self.setup_navigation()

        # Create main content frame
        self.main_frame = CTkFrame(self.main_container)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        if self.role == "admin":
            # Show dashboard initially only for admin
            self.show_dashboard()
        else:
            # For regular users, show the normal interface
            self.setup_user_interface()

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

        CTkButton(
            button_frame, text="Overdue Books", command=self.show_overdue_books
        ).pack(side="left", padx=5)

        self.setup_tree_view()

    def navigate_to(self, frame_func):
        # Add current frame to history before switching
        self.frame_history.append(self.current_frame)
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        # Show new frame
        frame_func()
        # Update current frame
        self.current_frame = frame_func

    def setup_navigation(self):
        # Only create navigation for admin role
        if self.role != "admin":
            return

        # Profile section
        profile_frame = CTkFrame(self.nav_frame)
        profile_frame.pack(fill="x", padx=10, pady=10)

        CTkLabel(
            profile_frame,
            text=f"Welcome Admin: {self.username}",
            font=("Helvetica", 16, "bold"),
        ).pack(pady=5)
        CTkLabel(
            profile_frame, text="Administrator Panel", font=("Helvetica", 12)
        ).pack()

        # Navigation buttons
        CTkButton(
            self.nav_frame,
            text="Dashboard",
            command=lambda: self.navigate_to(self.show_dashboard),
        ).pack(fill="x", padx=10, pady=5)
        CTkButton(
            self.nav_frame,
            text="Books Management",
            command=lambda: self.navigate_to(self.show_books_management),
        ).pack(fill="x", padx=10, pady=5)
        CTkButton(
            self.nav_frame,
            text="Admin Panel",
            command=lambda: self.navigate_to(self.show_admin_panel),
        ).pack(fill="x", padx=10, pady=5)
        CTkButton(
            self.nav_frame,
            text="Member Functions",
            command=lambda: self.navigate_to(self.show_member_functions),
        ).pack(fill="x", padx=10, pady=5)

        # General Navigation
        nav_label = CTkLabel(
            self.nav_frame, text="General Navigation", font=("Helvetica", 12, "bold")
        )
        nav_label.pack(pady=(20, 5))

        CTkButton(
            self.nav_frame,
            text="Home",
            command=lambda: self.navigate_to(self.show_dashboard),
        ).pack(fill="x", padx=10, pady=5)
        CTkButton(self.nav_frame, text="Back", command=self.go_back).pack(
            fill="x", padx=10, pady=5
        )
        CTkButton(self.nav_frame, text="Logout", command=self.logout).pack(
            fill="x", padx=10, pady=5
        )
        CTkButton(self.nav_frame, text="Exit", command=self.exit_app).pack(
            fill="x", padx=10, pady=5
        )

    def show_dashboard(self):
        if self.role != "admin":
            return

        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create dashboard header
        header = CTkLabel(
            self.main_frame, text="Admin Dashboard", font=("Helvetica", 24, "bold")
        )
        header.pack(pady=20)

        # Create stats container
        stats_container = CTkFrame(self.main_frame)
        stats_container.pack(fill="x", padx=20, pady=10)

        # Fetch statistics
        try:
            # Total books
            self.cursor.execute("SELECT COUNT(*) as total FROM Books")
            total_books = self.cursor.fetchone()["total"]

            # Books borrowed
            self.cursor.execute(
                """
                SELECT COUNT(*) as borrowed 
                FROM Books 
                WHERE availability_status = 'borrowed'
            """
            )
            borrowed_books = self.cursor.fetchone()["borrowed"]

            # Overdue books
            self.cursor.execute(
                """
                SELECT COUNT(*) as overdue 
                FROM Borrowing 
                WHERE returned_at IS NULL AND due_date < CURDATE()
            """
            )
            overdue_books = self.cursor.fetchone()["overdue"]

            # Total members
            self.cursor.execute("SELECT COUNT(*) as total FROM Members")
            total_members = self.cursor.fetchone()["total"]

            # Create stat cards
            self.create_stat_card(stats_container, "Total Books", total_books, "blue")
            self.create_stat_card(
                stats_container, "Books Borrowed", borrowed_books, "green"
            )
            self.create_stat_card(
                stats_container, "Overdue Books", overdue_books, "red"
            )
            self.create_stat_card(
                stats_container, "Total Members", total_members, "purple"
            )

            # Recent Activity Section
            activity_frame = CTkFrame(self.main_frame)
            activity_frame.pack(fill="x", padx=20, pady=20)

            CTkLabel(
                activity_frame, text="Recent Activity", font=("Helvetica", 18, "bold")
            ).pack(pady=10)

            # Create Treeview for recent activity
            columns = ("Action", "Book", "Member", "Date")
            activity_tree = ttk.Treeview(
                activity_frame, columns=columns, show="headings"
            )

            for col in columns:
                activity_tree.heading(col, text=col)
                activity_tree.column(col, width=150)

            # Fetch recent activity
            self.cursor.execute(
                """
                SELECT 
                    CASE 
                        WHEN b.returned_at IS NOT NULL THEN 'Return'
                        ELSE 'Borrow'
                    END as action,
                    bk.title,
                    u.username,
                    COALESCE(b.returned_at, b.borrowed_at) as action_date
                FROM Borrowing b
                JOIN Books bk ON b.book_id = bk.id
                JOIN Members m ON b.member_id = m.id
                JOIN Users u ON m.user_id = u.id
                ORDER BY COALESCE(b.returned_at, b.borrowed_at) DESC
                LIMIT 10
            """
            )

            activities = self.cursor.fetchall()
            for activity in activities:
                activity_tree.insert(
                    "",
                    "end",
                    values=(
                        activity["action"],
                        activity["title"],
                        activity["username"],
                        activity["action_date"],
                    ),
                )

            activity_tree.pack(fill="both", expand=True, padx=10, pady=10)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to load dashboard statistics: {e}")

    def create_stat_card(self, container, title, value, color):
        card = CTkFrame(container)
        card.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        CTkLabel(card, text=title, font=("Helvetica", 16)).pack(pady=5)
        CTkLabel(card, text=str(value), font=("Helvetica", 24, "bold")).pack(pady=5)

    def show_admin_panel(self):
        if self.role != "admin":
            return

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = CTkLabel(
            self.main_frame, text="Admin Control Panel", font=("Helvetica", 24, "bold")
        )
        header.pack(pady=20)

        # Create button container
        button_container = CTkFrame(self.main_frame)
        button_container.pack(fill="x", padx=20, pady=10)

        # Admin functions
        functions_frame = CTkFrame(button_container)
        functions_frame.pack(fill="x", padx=10, pady=10)

        CTkLabel(
            functions_frame, text="System Management", font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        functions = [
            ("Manage Users", self.manage_users),
            ("View All Fines", self.view_all_fines),
            ("System Settings", self.system_settings),
            ("Backup Database", self.backup_database),
            ("Generate Reports", self.generate_reports),
        ]

        for text, command in functions:
            CTkButton(functions_frame, text=text, command=command).pack(
                fill="x", padx=10, pady=5
            )

    def show_member_functions(self):
        if self.role != "admin":
            return

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = CTkLabel(
            self.main_frame,
            text="Member Functions Access",
            font=("Helvetica", 24, "bold"),
        )
        header.pack(pady=20)

        # Create button container
        button_container = CTkFrame(self.main_frame)
        button_container.pack(fill="x", padx=20, pady=10)

        # Member functions that admin can access
        CTkButton(button_container, text="Borrow Book", command=self.borrow_book).pack(
            side="left", padx=5
        )
        CTkButton(button_container, text="Return Book", command=self.return_book).pack(
            side="left", padx=5
        )
        CTkButton(button_container, text="Renew Book", command=self.renew_book).pack(
            side="left", padx=5
        )
        CTkButton(
            button_container,
            text="View Borrowed Books",
            command=self.view_borrowed_books,
        ).pack(side="left", padx=5)
        CTkButton(button_container, text="View Fines", command=self.view_fines).pack(
            side="left", padx=5
        )

        # Add the tree view for books
        self.setup_tree_view()

    def go_back(self):
        if self.frame_history:
            previous_frame = self.frame_history.pop()
            if previous_frame:
                for widget in self.main_frame.winfo_children():
                    widget.destroy()
                previous_frame()
                self.current_frame = previous_frame

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.quit()
            # Add your logout logic here

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.cleanup()
            self.root.quit()

    # this method i will implement in the future
    # Admin specific functions
    def manage_users(self):
        # Implement user management functionality
        pass

    def view_all_fines(self):
        # Implement fines overview functionality
        pass

    def system_settings(self):
        # Implement system settings functionality
        pass

    def backup_database(self):
        # Implement database backup functionality
        pass

    def generate_reports(self):
        # Implement report generation functionality
        pass

    def view_borrowed_books(self):
        # Implement borrowed books view functionality
        pass

    def view_fines(self):
        # Implement fines view functionality
        pass

    # here i implement this method(setup_tree_view, load_books, borrow_book, return_book, etc.)
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

    def return_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to return")
            return

        book_id = self.tree.item(selected[0])["values"][0]

        try:
            # Start transaction
            self.cursor.execute("START TRANSACTION")

            # Check if the book is borrowed by this user
            self.cursor.execute(
                """
                SELECT b.id, b.due_date, m.id as member_id 
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

            # Calculate fine if overdue
            due_date = datetime.strptime(str(borrowing["due_date"]), "%Y-%m-%d")
            today = datetime.now()
            fine_amount = 0

            if today.date() > due_date.date():
                days_overdue = (today.date() - due_date.date()).days
                fine_amount = days_overdue * 3  # $3 per day fine (fixed from $1)

                # Insert fine record if overdue
                if fine_amount > 0:
                    self.cursor.execute(
                        """
                        INSERT INTO Fines (borrowing_id, fine_amount, waived)
                        VALUES (%s, %s, FALSE)
                        """,
                        (borrowing["id"], fine_amount),
                    )

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
                SET returned_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (borrowing["id"],),
            )

            self.connection.commit()

            if fine_amount > 0:
                messagebox.showwarning(
                    "Fine Due",
                    f"Late return fine: ${fine_amount:.2f}\n({days_overdue} days overdue at $3/day)",
                )
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

    def run(self):
        self.root.mainloop()

    def cleanup(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def __del__(self):
        self.cleanup()

    def show_books_management(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = CTkLabel(
            self.main_frame, text="Books Management", font=("Helvetica", 24, "bold")
        )
        header.pack(pady=20)

        top_frame = CTkFrame(self.main_frame)
        top_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = CTkEntry(top_frame, placeholder_text="Search books...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        CTkButton(top_frame, text="Search", command=self.search_books).pack(
            side="left", padx=5
        )

        buttons_frame = CTkFrame(self.main_frame)
        buttons_frame.pack(fill="x", padx=20, pady=10)

        if self.role == "admin":
            CTkButton(
                buttons_frame, text="Add Book", command=self.add_book_window
            ).pack(side="left", padx=5)
            CTkButton(
                buttons_frame, text="Modify Book", command=self.modify_book_window
            ).pack(side="left", padx=5)
            CTkButton(buttons_frame, text="Delete Book", command=self.delete_book).pack(
                side="left", padx=5
            )
            CTkButton(
                buttons_frame, text="Delete All", command=self.delete_all_books
            ).pack(side="left", padx=5)
            CTkButton(
                buttons_frame, text="Overdue Books", command=self.show_overdue_books
            ).pack(side="left", padx=5)
        else:
            CTkButton(buttons_frame, text="Borrow Book", command=self.borrow_book).pack(
                side="left", padx=5
            )
            CTkButton(buttons_frame, text="Return Book", command=self.return_book).pack(
                side="left", padx=5
            )
            CTkButton(buttons_frame, text="Renew Book", command=self.renew_book).pack(
                side="left", padx=5
            )

        tree_frame = CTkFrame(self.main_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Title", "Author", "ISBN", "Publication Date", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_books()

    def search_books(self):
        query = self.search_entry.get()
        try:
            if query:
                self.cursor.execute(
                    """
                    SELECT b.id, b.title, GROUP_CONCAT(ba.author) as authors, 
                        b.isbn, b.publication_date, b.availability_status
                    FROM Books b
                    LEFT JOIN book_author ba ON b.id = ba.book_id
                    WHERE b.title LIKE %s OR ba.author LIKE %s OR b.isbn LIKE %s
                    GROUP BY b.id
                """,
                    (f"%{query}%", f"%{query}%", f"%{query}%"),
                )
            else:
                self.cursor.execute(
                    """
                    SELECT b.id, b.title, GROUP_CONCAT(ba.author) as authors, 
                        b.isbn, b.publication_date, b.availability_status
                    FROM Books b
                    LEFT JOIN book_author ba ON b.id = ba.book_id
                    GROUP BY b.id
                """
                )

            for item in self.tree.get_children():
                self.tree.delete(item)

            for book in self.cursor.fetchall():
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        book["id"],
                        book["title"],
                        book["authors"] or "Unknown",
                        book["isbn"],
                        book["publication_date"],
                        book["availability_status"],
                    ),
                )
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to search books: {e}")

    def load_books(self):
        try:
            self.cursor.execute(
                """
                SELECT b.id, b.title, GROUP_CONCAT(ba.author) as authors, 
                    b.isbn, b.publication_date, b.availability_status
                FROM Books b
                LEFT JOIN book_author ba ON b.id = ba.book_id
                GROUP BY b.id
            """
            )

            for item in self.tree.get_children():
                self.tree.delete(item)

            for book in self.cursor.fetchall():
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        book["id"],
                        book["title"],
                        book["authors"] or "Unknown",
                        book["isbn"],
                        book["publication_date"],
                        book["availability_status"],
                    ),
                )
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")

    def create_admin_buttons(self, buttons_frame):
        CTkButton(buttons_frame, text="Add Book", command=self.add_book_window).pack(
            side="left", padx=5
        )
        CTkButton(
            buttons_frame, text="Modify Book", command=self.modify_book_window
        ).pack(side="left", padx=5)
        CTkButton(buttons_frame, text="Delete Book", command=self.delete_book).pack(
            side="left", padx=5
        )
        CTkButton(buttons_frame, text="Delete All", command=self.delete_all_books).pack(
            side="left", padx=5
        )
        CTkButton(
            buttons_frame, text="Overdue Books", command=self.show_overdue_books
        ).pack(side="left", padx=5)

    def create_user_buttons(self, buttons_frame):
        CTkButton(buttons_frame, text="Borrow Book", command=self.borrow_book).pack(
            side="left", padx=5
        )
        CTkButton(buttons_frame, text="Buy Book", command=self.buy_book).pack(
            side="left", padx=5
        )
        CTkButton(buttons_frame, text="Return Book", command=self.return_book).pack(
            side="left", padx=5
        )
        CTkButton(buttons_frame, text="Renew Book", command=self.renew_book).pack(
            side="left", padx=5
        )

    def add_book_window(self):
        add_window = CTkToplevel(self.root)
        add_window.title("Add New Book")
        add_window.geometry("400x600")

        fields = {
            "Title": "",
            "Authors": "",  # Changed to Authors (comma-separated)
            "ISBN": "",
            "Publication Date": "",
            "Genre": "",
            "Status": "available",
        }
        entries = {}

        for field in fields:
            CTkLabel(add_window, text=field).pack(pady=5)
            entries[field] = CTkEntry(add_window)
            entries[field].insert(0, fields[field])
            entries[field].pack(pady=5)

        def save_book():
            try:
                # Start a transaction
                self.cursor.execute("START TRANSACTION")

                # Insert into Books table
                self.cursor.execute(
                    """
                    INSERT INTO Books (title, isbn, publication_date, genre, availability_status)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        entries["Title"].get(),
                        entries["ISBN"].get(),
                        entries["Publication Date"].get(),
                        entries["Genre"].get(),
                        entries["Status"].get(),
                    ),
                )

                # Get the last inserted book ID
                book_id = self.cursor.lastrowid

                # Handle authors (split by comma and insert into book_author table)
                authors = [
                    author.strip() for author in entries["Authors"].get().split(",")
                ]
                for author in authors:
                    if author:  # Only insert non-empty author names
                        self.cursor.execute(
                            """
                            INSERT INTO book_author (book_id, author)
                            VALUES (%s, %s)
                            """,
                            (book_id, author),
                        )

                self.connection.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                add_window.destroy()
                self.load_books()

            except mysql.connector.Error as e:
                self.connection.rollback()
                messagebox.showerror("Error", f"Failed to add book: {e}")

        CTkButton(add_window, text="Save Book", command=save_book).pack(pady=20)

    def modify_book_window(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Please select a book to modify")
            return

        selected_item = self.tree.selection()[0]
        book_data = self.tree.item(selected_item)["values"]
        book_id = book_data[0]

        # Fetch current book data including authors
        try:
            self.cursor.execute(
                """
                SELECT b.*, GROUP_CONCAT(ba.author) as authors
                FROM Books b
                LEFT JOIN book_author ba ON b.id = ba.book_id
                WHERE b.id = %s
                GROUP BY b.id
                """,
                (book_id,),
            )
            current_book = self.cursor.fetchone()

            modify_window = CTkToplevel(self.root)
            modify_window.title("Modify Book")
            modify_window.geometry("400x600")

            fields = {
                "Title": current_book["title"],
                "Authors": current_book["authors"] or "",
                "ISBN": current_book["isbn"],
                "Publication Date": current_book["publication_date"],
                "Genre": current_book["genre"] or "",
                "Status": current_book["availability_status"],
            }
            entries = {}

            for field in fields:
                CTkLabel(modify_window, text=field).pack(pady=5)
                entries[field] = CTkEntry(modify_window)
                entries[field].insert(0, fields[field])
                entries[field].pack(pady=5)

            def save_modifications():
                try:
                    # Start transaction
                    self.cursor.execute("START TRANSACTION")

                    # Update Books table
                    self.cursor.execute(
                        """
                        UPDATE Books 
                        SET title=%s, isbn=%s, publication_date=%s, genre=%s, availability_status=%s
                        WHERE id=%s
                        """,
                        (
                            entries["Title"].get(),
                            entries["ISBN"].get(),
                            entries["Publication Date"].get(),
                            entries["Genre"].get(),
                            entries["Status"].get(),
                            book_id,
                        ),
                    )

                    # Update authors
                    # First, delete all existing authors for this book
                    self.cursor.execute(
                        "DELETE FROM book_author WHERE book_id=%s", (book_id,)
                    )

                    # Then insert new authors
                    authors = [
                        author.strip() for author in entries["Authors"].get().split(",")
                    ]
                    for author in authors:
                        if author:  # Only insert non-empty author names
                            self.cursor.execute(
                                """
                                INSERT INTO book_author (book_id, author)
                                VALUES (%s, %s)
                                """,
                                (book_id, author),
                            )

                    self.connection.commit()
                    messagebox.showinfo("Success", "Book modified successfully!")
                    modify_window.destroy()
                    self.load_books()

                except mysql.connector.Error as e:
                    self.connection.rollback()
                    messagebox.showerror("Error", f"Failed to modify book: {e}")

            CTkButton(
                modify_window, text="Save Changes", command=save_modifications
            ).pack(pady=20)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to fetch book details: {e}")

    def calculate_fine(self, borrowing_id):
        """Calculate fine amount based on overdue days"""
        try:
            # First check if the borrowing exists and get relevant dates
            self.cursor.execute(
                """
                SELECT 
                    due_date,
                    returned_at,
                    DATEDIFF(
                        COALESCE(returned_at, CURRENT_TIMESTAMP()),
                        due_date
                    ) as overdue_days
                FROM Borrowing
                WHERE id = %s
                """,
                (borrowing_id,),
            )
            result = self.cursor.fetchone()

            if not result:
                print(f"No borrowing found for ID: {borrowing_id}")
                return 0

            # For debugging
            print(f"Due date: {result['due_date']}")
            print(f"Returned at: {result['returned_at']}")
            print(f"Overdue days: {result['overdue_days']}")

            if result["overdue_days"] > 0:
                fine_amount = result["overdue_days"] * 3  # $3 per day

                # Start transaction
                self.cursor.execute("START TRANSACTION")

                try:
                    # First check if fine already exists
                    self.cursor.execute(
                        """
                        SELECT id FROM Fines 
                        WHERE borrowing_id = %s
                        """,
                        (borrowing_id,),
                    )
                    existing_fine = self.cursor.fetchone()

                    if existing_fine:
                        # Update existing fine
                        self.cursor.execute(
                            """
                            UPDATE Fines 
                            SET fine_amount = %s,
                                created_at = CURRENT_TIMESTAMP()
                            WHERE borrowing_id = %s
                            """,
                            (fine_amount, borrowing_id),
                        )
                    else:
                        # Insert new fine
                        self.cursor.execute(
                            """
                            INSERT INTO Fines (borrowing_id, fine_amount, waived)
                            VALUES (%s, %s, FALSE)
                            """,
                            (borrowing_id, fine_amount),
                        )

                    self.connection.commit()
                    print(f"Fine amount calculated and saved: ${fine_amount}")
                    return fine_amount

                except mysql.connector.Error as e:
                    self.connection.rollback()
                    print(f"Error saving fine amount: {e}")
                    messagebox.showerror("Error", f"Failed to save fine: {e}")
                    return 0

            return 0

        except mysql.connector.Error as e:
            print(f"Error calculating fine: {e}")
            messagebox.showerror("Error", f"Failed to calculate fine: {e}")
            return 0

    def delete_book(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Please select a book to delete")
            return

        if messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this book?"
        ):
            selected_item = self.tree.selection()[0]
            book_id = self.tree.item(selected_item)["values"][0]

            try:
                self.cursor.execute("DELETE FROM Books WHERE id=%s", (book_id,))
                self.connection.commit()
                self.tree.delete(selected_item)
                messagebox.showinfo("Success", "Book deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete book: {e}")

    def delete_all_books(self):
        if messagebox.askyesno(
            "Confirm Delete All",
            "Are you sure you want to delete ALL books? This cannot be undone!",
        ):
            try:
                self.cursor.execute("DELETE FROM Books")
                self.connection.commit()
                self.load_books()
                messagebox.showinfo("Success", "All books deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete all books: {e}")

    def show_overdue_books(self):
        try:
            self.cursor.execute(
                """
                SELECT b.title, u.username, br.borrowed_at, br.due_date, f.fine_amount
                FROM Books b
                JOIN Borrowing br ON b.id = br.book_id
                JOIN Members m ON br.member_id = m.id
                JOIN Users u ON m.user_id = u.id
                LEFT JOIN Fines f ON br.id = f.borrowing_id
                WHERE br.returned_at IS NULL AND br.due_date < CURDATE()
            """
            )

            overdue_window = CTkToplevel(self.root)
            overdue_window.title("Overdue Books")
            overdue_window.geometry("800x400")

            columns = (
                "Book Title",
                "Borrowed By",
                "Borrowed Date",
                "Due Date",
                "Fine Amount",
            )
            tree = ttk.Treeview(overdue_window, columns=columns, show="headings")

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            for book in self.cursor.fetchall():
                fine_amount = book["fine_amount"] if book["fine_amount"] else 0
                tree.insert(
                    "",
                    "end",
                    values=(
                        book["title"],
                        book["username"],
                        book["borrowed_at"],
                        book["due_date"],
                        f"${fine_amount:.2f}",
                    ),
                )

            tree.pack(fill="both", expand=True, padx=10, pady=10)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Failed to fetch overdue books: {e}")


# Main execution
if __name__ == "__main__":
    app = LibrarySystem(role="admin", username="test_user")
    try:
        app.run()
    finally:
        app.cleanup()
