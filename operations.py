# operations.py - Library Management System Core Functions

# Data Structures
books = []  # List to store book dictionaries
members = []  # List to store member dictionaries
VALID_GENRES = ("Fiction", "Non-Fiction", "Sci-Fi")  # Tuple of valid genres


# ===== BOOK OPERATIONS =====

def add_book(isbn, title, author, genre, total_copies):
    """Add a new book to the library system"""
    # Check if ISBN is unique
    for book in books:
        if book["isbn"] == isbn:
            return "Error: ISBN already exists"

    # Check if genre is valid
    if genre not in VALID_GENRES:
        return f"Error: Genre must be one of {VALID_GENRES}"

    # Create book dictionary
    new_book = {
        "isbn": isbn,
        "title": title,
        "author": author,
        "genre": genre,
        "total_copies": total_copies,
        "available_copies": total_copies
    }

    books.append(new_book)
    return f"Book '{title}' added successfully"


def search_books(search_term):
    """Search books by title or author"""
    results = []
    search_lower = search_term.lower()

    for book in books:
        if search_lower in book["title"].lower() or search_lower in book["author"].lower():
            results.append(book)

    return results


def update_book(isbn, title=None, author=None, genre=None, total_copies=None):
    """Update book details"""
    for book in books:
        if book["isbn"] == isbn:
            if title:
                book["title"] = title
            if author:
                book["author"] = author
            if genre:
                if genre in VALID_GENRES:
                    book["genre"] = genre
                else:
                    return f"Error: Genre must be one of {VALID_GENRES}"
            if total_copies is not None:
                book["total_copies"] = total_copies
            return f"Book with ISBN {isbn} updated successfully"

    return "Error: Book not found"


def delete_book(isbn):
    """Delete a book only if no copies are borrowed"""
    for book in books:
        if book["isbn"] == isbn:
            if book["available_copies"] < book["total_copies"]:
                return "Error: Cannot delete book with borrowed copies"
            books.remove(book)
            return f"Book with ISBN {isbn} deleted successfully"

    return "Error: Book not found"


# ===== MEMBER OPERATIONS =====

def add_member(member_id, name, email, contact):
    """Add a new member to the library system"""
    # Check if member ID is unique
    for member in members:
        if member["id"] == member_id:
            return "Error: Member ID already exists"

    # Create member dictionary
    new_member = {
        "id": member_id,
        "name": name,
        "email": email,
        "contact": contact,
        "borrowed_books": []  # List to track borrowed book ISBNs
    }

    members.append(new_member)
    return f"Member '{name}' added successfully"


def update_member(member_id, name=None, email=None, contact=None):
    """Update member details"""
    for member in members:
        if member["id"] == member_id:
            if name:
                member["name"] = name
            if email:
                member["email"] = email
            if contact:
                member["contact"] = contact
            return f"Member with ID {member_id} updated successfully"

    return "Error: Member not found"


def delete_member(member_id):
    """Delete a member only if they have no borrowed books"""
    for member in members:
        if member["id"] == member_id:
            if len(member["borrowed_books"]) > 0:
                return "Error: Cannot delete member with borrowed books"
            members.remove(member)
            return f"Member with ID {member_id} deleted successfully"

    return "Error: Member not found"


# ===== BORROW/RETURN OPERATIONS =====

def borrow_book(member_id, isbn):
    """Allow a member to borrow a book"""
    # Find member
    member = None
    for m in members:
        if m["id"] == member_id:
            member = m
            break

    if not member:
        return "Error: Member not found"

    # Check if member already has 3 books
    if len(member["borrowed_books"]) >= 3:
        return "Error: Member has already borrowed 3 books"

    # Find book
    book = None
    for b in books:
        if b["isbn"] == isbn:
            book = b
            break

    if not book:
        return "Error: Book not found"

    # Check if book is available
    if book["available_copies"] <= 0:
        return "Error: No copies available"

    # Borrow the book
    member["borrowed_books"].append(isbn)
    book["available_copies"] -= 1
    return f"Book '{book['title']}' borrowed successfully by {member['name']}"


def return_book(member_id, isbn):
    """Allow a member to return a borrowed book"""
    # Find member
    member = None
    for m in members:
        if m["id"] == member_id:
            member = m
            break

    if not member:
        return "Error: Member not found"

    # Check if member has borrowed this book
    if isbn not in member["borrowed_books"]:
        return "Error: Member has not borrowed this book"

    # Find book
    book = None
    for b in books:
        if b["isbn"] == isbn:
            book = b
            break

    if not book:
        return "Error: Book not found"

    # Return the book
    member["borrowed_books"].remove(isbn)
    book["available_copies"] += 1
    return f"Book '{book['title']}' returned successfully by {member['name']}"


# ===== DISPLAY FUNCTIONS =====

def display_all_books():
    """Display all books in the library"""
    if not books:
        return "No books in the library"

    print("\n=== ALL BOOKS ===")
    for book in books:
        print(f"ISBN: {book['isbn']}, Title: {book['title']}, Author: {book['author']}, "
              f"Genre: {book['genre']}, Available: {book['available_copies']}/{book['total_copies']}")
    return ""


def display_all_members():
    """Display all members"""
    if not members:
        return "No members registered"

    print("\n=== ALL MEMBERS ===")
    for member in members:
        print(f"ID: {member['id']}, Name: {member['name']}, Email: {member['email']}, "
              f"Borrowed Books: {len(member['borrowed_books'])}")
    return ""


# ===== INTERACTIVE MENU SYSTEM =====

def show_menu():
    """Display the main menu"""
    print("\n" + "=" * 60)
    print("LIBRARY MANAGEMENT SYSTEM")
    print("=" * 60)
    print("\n📚 BOOK OPERATIONS:")
    print("  1. Add New Book")
    print("  2. Search Books")
    print("  3. Update Book")
    print("  4. Delete Book")
    print("  5. Display All Books")
    print("\n👥 MEMBER OPERATIONS:")
    print("  6. Add New Member")
    print("  7. Update Member")
    print("  8. Delete Member")
    print("  9. Display All Members")
    print("\n📖 BORROW/RETURN OPERATIONS:")
    print("  10. Borrow Book")
    print("  11. Return Book")
    print("\n  0. Exit System")
    print("=" * 60)


def main():
    """Main interactive program"""
    print("\n🎓 Welcome to Library Management System!")
    print("Valid Genres: Fiction, Non-Fiction, Sci-Fi")

    while True:
        show_menu()
        choice = input("\nEnter your choice (0-11): ").strip()

        if choice == "1":
            # Add Book
            print("\n--- ADD NEW BOOK ---")
            isbn = input("Enter ISBN: ").strip()
            title = input("Enter Title: ").strip()
            author = input("Enter Author: ").strip()
            genre = input("Enter Genre (Fiction/Non-Fiction/Sci-Fi): ").strip()
            total_copies = input("Enter Total Copies: ").strip()

            try:
                total_copies = int(total_copies)
                result = add_book(isbn, title, author, genre, total_copies)
                print(f"\n✓ {result}")
            except ValueError:
                print("\n✗ Error: Total copies must be a number!")

        elif choice == "2":
            # Search Books
            print("\n--- SEARCH BOOKS ---")
            search_term = input("Enter title or author to search: ").strip()
            results = search_books(search_term)

            if results:
                print(f"\n✓ Found {len(results)} book(s):")
                for book in results:
                    print(
                        f"  - ISBN: {book['isbn']}, Title: {book['title']}, Author: {book['author']}, Genre: {book['genre']}")
            else:
                print("\n✗ No books found matching your search.")

        elif choice == "3":
            # Update Book
            print("\n--- UPDATE BOOK ---")
            isbn = input("Enter ISBN of book to update: ").strip()
            print("Leave blank to keep current value")
            title = input("New Title (or press Enter): ").strip() or None
            author = input("New Author (or press Enter): ").strip() or None
            genre = input("New Genre (or press Enter): ").strip() or None
            total_copies = input("New Total Copies (or press Enter): ").strip()

            try:
                total_copies = int(total_copies) if total_copies else None
                result = update_book(isbn, title, author, genre, total_copies)
                print(f"\n✓ {result}")
            except ValueError:
                print("\n✗ Error: Total copies must be a number!")

        elif choice == "4":
            # Delete Book
            print("\n--- DELETE BOOK ---")
            isbn = input("Enter ISBN of book to delete: ").strip()
            confirm = input(f"Are you sure you want to delete book {isbn}? (yes/no): ").strip().lower()

            if confirm == "yes":
                result = delete_book(isbn)
                print(f"\n✓ {result}")
            else:
                print("\n✗ Deletion cancelled.")

        elif choice == "5":
            # Display All Books
            display_all_books()

        elif choice == "6":
            # Add Member
            print("\n--- ADD NEW MEMBER ---")
            member_id = input("Enter Member ID: ").strip()
            name = input("Enter Name: ").strip()
            email = input("Enter Email: ").strip()
            contact = input("Enter Contact: ").strip()

            result = add_member(member_id, name, email, contact)
            print(f"\n✓ {result}")

        elif choice == "7":
            # Update Member
            print("\n--- UPDATE MEMBER ---")
            member_id = input("Enter Member ID to update: ").strip()
            print("Leave blank to keep current value")
            name = input("New Name (or press Enter): ").strip() or None
            email = input("New Email (or press Enter): ").strip() or None
            contact = input("New Contact (or press Enter): ").strip() or None

            result = update_member(member_id, name, email, contact)
            print(f"\n✓ {result}")

        elif choice == "8":
            # Delete Member
            print("\n--- DELETE MEMBER ---")
            member_id = input("Enter Member ID to delete: ").strip()
            confirm = input(f"Are you sure you want to delete member {member_id}? (yes/no): ").strip().lower()

            if confirm == "yes":
                result = delete_member(member_id)
                print(f"\n✓ {result}")
            else:
                print("\n✗ Deletion cancelled.")

        elif choice == "9":
            # Display All Members
            display_all_members()

        elif choice == "10":
            # Borrow Book
            print("\n--- BORROW BOOK ---")
            member_id = input("Enter Member ID: ").strip()
            isbn = input("Enter Book ISBN: ").strip()

            result = borrow_book(member_id, isbn)
            print(f"\n✓ {result}")

        elif choice == "11":
            # Return Book
            print("\n--- RETURN BOOK ---")
            member_id = input("Enter Member ID: ").strip()
            isbn = input("Enter Book ISBN: ").strip()

            result = return_book(member_id, isbn)
            print(f"\n✓ {result}")

        elif choice == "0":
            # Exit
            print("\n" + "=" * 60)
            print("Thank you for using Library Management System!")
            print("Goodbye! 👋")
            print("=" * 60)
            break

        else:
            print("\n✗ Invalid choice! Please enter a number between 0-11.")

        # Pause before showing menu again
        input("\nPress Enter to continue...")


# ===== RUN PROGRAM =====

if __name__ == "__main__":
    main()