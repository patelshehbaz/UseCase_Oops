from datetime import datetime, timedelta

class Book:
    def __init__(self, isbn, title, subject, publisher, authors):
        self.isbn = isbn
        self.title = title
        self.subject = subject
        self.publisher = publisher
        self.authors = authors

class BookItem(Book):
    def __init__(self, isbn, title, subject, publisher, authors, barcode, rack):
        super().__init__(isbn, title, subject, publisher, authors)
        self.barcode = barcode
        self.rack = rack
        self.is_checked_out = False
        self.due_date = None
        self.borrower = None

    def checkout(self, borrower, days=10):
        if not self.is_checked_out:
            self.is_checked_out = True
            self.due_date = datetime.now() + timedelta(days=days)
            self.borrower = borrower
            print(f"Book {self.title} checked out by {borrower.name}, due on {self.due_date}.")
        else:
            print(f"Book {self.title} is already checked out.")

    def return_book(self):
        if self.is_checked_out:
            self.is_checked_out = False
            overdue_days = (datetime.now() - self.due_date).days
            self.due_date = None
            self.borrower = None
            if overdue_days > 0:
                print(f"Book {self.title} returned late. Fine applicable for {overdue_days} days.")
            else:
                print(f"Book {self.title} returned on time.")
        else:
            print(f"Book {self.title} was not checked out.")

class Account:
    def __init__(self, name, library_card):
        self.name = name
        self.library_card = library_card
        self.checked_out_books = []
        self.reserved_books = []
        self.max_books = 5

    def check_out_book(self, book_item):
        if len(self.checked_out_books) >= self.max_books:
            print(f"Cannot check out more than {self.max_books} books.")
            return

        if book_item.is_checked_out:
            print(f"Book {book_item.title} is already checked out.")
        else:
            book_item.checkout(self)
            self.checked_out_books.append(book_item)

    def return_book(self, book_item):
        if book_item in self.checked_out_books:
            book_item.return_book()
            self.checked_out_books.remove(book_item)
        else:
            print(f"Book {book_item.title} was not checked out by {self.name}.")

    def reserve_book(self, book_item):
        if book_item.is_checked_out:
            self.reserved_books.append(book_item)
            print(f"Book {book_item.title} reserved by {self.name}.")
        else:
            print(f"Book {book_item.title} is available and can be checked out.")

class LibraryCard:
    def __init__(self, card_number):
        self.card_number = card_number

class Library:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.books = []
        self.accounts = []

    def add_book(self, book_item):
        self.books.append(book_item)
        print(f"Book {book_item.title} added to the library.")

    def add_account(self, account):
        self.accounts.append(account)
        print(f"Account for {account.name} added.")

    def search_books(self, title=None, author=None, subject=None):
        results = []
        for book in self.books:
            if (title and title.lower() in book.title.lower()) or \
               (author and any(author.lower() in a.lower() for a in book.authors)) or \
               (subject and subject.lower() in book.subject.lower()):
                results.append(book)
        return results

    def get_overdue_books(self):
        overdue_books = []
        for book in self.books:
            if book.is_checked_out and book.due_date < datetime.now():
                overdue_books.append(book)
        return overdue_books

    def send_notification(self, account, message):
        print(f"Notification sent to {account.name}: {message}")

class Fine:
    @staticmethod
    def calculate_fine(days_overdue):
        fine_per_day = 1  # Example rate
        return days_overdue * fine_per_day

# Function for user interaction
def main():
    library = Library("Central Library", "123 Library St.")

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Add Account")
        print("3. Check Out Book")
        print("4. Return Book")
        print("5. Reserve Book")
        print("6. Search Books")
        print("7. View Overdue Books")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            isbn = input("Enter ISBN: ")
            title = input("Enter Title: ")
            subject = input("Enter Subject: ")
            publisher = input("Enter Publisher: ")
            authors = input("Enter Authors (comma separated): ").split(", ")
            barcode = input("Enter Barcode: ")
            rack = input("Enter Rack: ")

            book_item = BookItem(isbn, title, subject, publisher, authors, barcode, rack)
            library.add_book(book_item)

        elif choice == '2':
            name = input("Enter Member Name: ")
            card_number = input("Enter Library Card Number: ")

            card = LibraryCard(card_number)
            account = Account(name, card)
            library.add_account(account)

        elif choice == '3':
            card_number = input("Enter Library Card Number: ")
            barcode = input("Enter Book Barcode: ")

            account = next((acc for acc in library.accounts if acc.library_card.card_number == card_number), None)
            book_item = next((bk for bk in library.books if bk.barcode == barcode), None)

            if account and book_item:
                account.check_out_book(book_item)
            else:
                print("Invalid account or book.")

        elif choice == '4':
            card_number = input("Enter Library Card Number: ")
            barcode = input("Enter Book Barcode: ")

            account = next((acc for acc in library.accounts if acc.library_card.card_number == card_number), None)
            book_item = next((bk for bk in library.books if bk.barcode == barcode), None)

            if account and book_item:
                account.return_book(book_item)
            else:
                print("Invalid account or book.")

        elif choice == '5':
            card_number = input("Enter Library Card Number: ")
            barcode = input("Enter Book Barcode: ")

            account = next((acc for acc in library.accounts if acc.library_card.card_number == card_number), None)
            book_item = next((bk for bk in library.books if bk.barcode == barcode), None)

            if account and book_item:
                account.reserve_book(book_item)
            else:
                print("Invalid account or book.")

        elif choice == '6':
            title = input("Enter Title (leave blank if not searching by title): ")
            author = input("Enter Author (leave blank if not searching by author): ")
            subject = input("Enter Subject (leave blank if not searching by subject): ")

            results = library.search_books(title, author, subject)
            if results:
                print("\nSearch Results:")
                for book in results:
                    print(f"Title: {book.title}, Authors: {', '.join(book.authors)}, Subject: {book.subject}")
            else:
                print("No books found.")

        elif choice == '7':
            overdue_books = library.get_overdue_books()
            if overdue_books:
                print("\nOverdue Books:")
                for book in overdue_books:
                    days_overdue = (datetime.now() - book.due_date).days
                    fine = Fine.calculate_fine(days_overdue)
                    print(f"Title: {book.title}, Borrower: {book.borrower.name}, Fine: ${fine}")
            else:
                print("No overdue books.")

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")

# Run the main function
if __name__ == "__main__":
    main()