from itertools import count


class Book:
    _ids = count(1)

    def __init__(self, title, number_of_copies):
        self.id = next(self._ids)
        self.title = title
        self.number_of_copies = number_of_copies
        self.member_borrowing = []

    def add_borrower(self, member):
        self.member_borrowing.append(member)


class Member:
    _ids = count(1)

    def __init__(self, name):
        self.name = name
        self.id = next(self._ids)
        self.borrowed_books = []

    def add_borrowed_book(self, book):
        self.borrowed_books.append(book)


def menu_options():
    print('''Main Menu - please select an option:
    1) Add new member
    2) Add new book
    3) Process borrowing
    4) Process returning
    5) View member status
    6) View book status
    7) Quit''')


def continue_process(question, continue_process, go_back, feedback):
    global add_flag
    continue_member = True
    while continue_member:
        member_selection = input(
            question)
        if member_selection == continue_process:

            add_flag = True
            continue_member = False
        elif member_selection == go_back:

            add_flag = False
            continue_member = False

        else:
            print(feedback)
            continue_member = True


def add_member():
    global array_list_member
    global add_flag
    add_flag = True
    while add_flag:
        member_name = input("Please enter the name of new member: \n")
        array_list_member.append(Member(member_name))
        new_member = array_list_member[len(array_list_member) - 1]
        print(f"Member [{new_member.name}] has been created with member ID: [{new_member.id}]")
        continue_process("Would you like to [a]dd a new member or go-[b]ack to the previous menu?", "a",
                         "b",
                         "Invalid selection please enter [a] to add new member or [b] to go back to menu\n")


def validate(prompt, exception):
    invalid_input = True
    while invalid_input:
        try:
            valid_input = int(input(prompt))
            if valid_input > 0:
                invalid_input = False

            else:
                invalid_input = True
                print(exception)

        except ValueError:
            print(exception)
            invalid_input = True
    return valid_input


def process_return():
    global array_list_member
    global add_flag
    add_flag = True
    book_in_browed_books = True
    member_exist = False
    while add_flag:

        member_id = validate("Please enter a valid member ID:\n", "A valid member id is a positive integer number")
        for member in array_list_member:
            if member.id == member_id:
                member_exist = True

                book_id = validate(f"Please enter a valid book ID for returning by member [{member.name}]\n",
                                   "A valid book id is a positive integer number")

                for book in member.borrowed_books:
                    if book_id == book.id:
                        book.number_of_copies = book.number_of_copies + 1
                        index = member.borrowed_books.index(book)
                        del member.borrowed_books[index]
                        print(f"*** Returning processed successfully***\n"
                              f"Member:{member.name}\n"
                              f"Book returned:{book.title}\n"
                              f"After returning Number of books [{book.title}] available in stock:{book.number_of_copies}\n")
                        continue_process(
                            " Would you like to [p]rocess a new returning or go-[b]ack to the previous menu?\n", "p",
                            "b",
                            "Invalid selection please enter [p] to process a new returning or [b] to go back to menu\n")
                        book_in_browed_books = True
                        break
                    else:
                        book_in_browed_books = False
                if not book_in_browed_books:
                    print(f"Book with id[{book_id} not in member [{member.name}] borrowed books]")
            else:
                member_exist = False
        if not member_exist:
            print(f"Member with id[{member_id}] does not exist")


def add_book():
    global array_list_book

    global add_flag
    add_flag = True
    while add_flag:

        is_book_unique = False
        while not is_book_unique:
            book_title = input("Please enter the name of book: \n")
            if len(array_list_book) > 0:
                for book in array_list_book:
                    if book.title == book_title:
                        is_book_unique = False
                        print(f"Book with title {book_title} already exists...please enter another book")
                    else:
                        is_book_unique = True

            else:
                is_book_unique = True

        error = True
        while error:
            try:
                book_number_of_copies = int(input("Please enter number of copies\n "))
                if book_number_of_copies > 0:
                    array_list_book.append(Book(book_title, book_number_of_copies))
                    new_book = array_list_book[len(array_list_book) - 1]
                    print(f"\nNew Book Added :\n"
                          f"BookId: {new_book.id}\n"
                          f"Book Title: {new_book.title}\n"
                          f"Number of copies: {new_book.number_of_copies}\n")
                    continue_process(
                        'Would you like to [a]dd a new book or go-[b]ack to the previous menu?\n', 'a', 'b',
                        "Invalid selection please enter [a] to add new book or [b] to go back to menu\n")
                    error = False
                else:

                    print("Number of copies must be Zero or a positive integer\n")
                    error = True
            except ValueError:
                print("Number of copies must be Zero or a positive integer\n")
                error = True


def welcome_banner():
    print('''
--------------------------------------------------------
---Welcome To ITECH 5403 Library Management System---
--------------------------------------------------------''')


def process_borrowing():
    global array_list_member
    global array_list_book
    book_exist_flag = True
    member_exist_flag = True

    member_id = validate("Please enter a valid member ID:\n", "A valid member ID must be a positive integer")

    for member in array_list_member:
        if member.id == member_id:
            member_exist_flag = True

            book_id = validate(f"Please enter a valid book ID for borrowing by member [{member.name}]:",
                               "A valid book ID must be a positive integer")

            for book in array_list_book:
                if book.id == book_id and book.number_of_copies > 0:
                    book.add_borrower(member)
                    book.number_of_copies = book.number_of_copies - 1
                    member.add_borrowed_book(book)
                    print(f"*** Borrowing processed successfully***\n"
                          f"Member:{member.name}\n"
                          f"Borrowed Book title: {book.title}\n"
                          f"Number of books remaining: {book.number_of_copies}\n ")
                    break
                elif book.id == book_id and book.number_of_copies <= 0:
                    print(f"Sorry!!! Book titled [{book.title}] currently is not available for borrowing.")
                    break
                elif book_id != book.id:
                    book_exist_flag = False;
            if not book_exist_flag:
                print("Book does not exist")
        else:
            member_exist_flag = False
    if not member_exist_flag:
        print(f"Member with id[{member_id}] does not exist")


def view_member_status():
    global array_list_member
    global borrowed_books_empty_flag
    global add_flag
    add_flag = True
    while add_flag:
        member_id = validate("Please enter a valid member ID:\n", "A valid member ID must be a positive integer")
        if len(array_list_member) > 0:
            for member in array_list_member:
                if member_id == member.id:
                    titles_borrowed_books = []
                    print(f"Member[{member.id}]: {member.name}")
                    borrowed_books_empty_flag = False
                    if len(member.borrowed_books) > 0:
                        borrowed_books_empty_flag = False
                        for book in member.borrowed_books:
                            titles_borrowed_books.append(book.title)
                    else:
                        borrowed_books_empty_flag = True
                    if borrowed_books_empty_flag:
                        print("Borrowed books: None")
                        continue_process(
                            "  Would you like to view a new member’s [s]tatus or go-[b]ack to the previous menu?\n",
                            "s",
                            "b",
                            "Invalid selection please enter [s] to view a new member's status or [b] to go back to menu\n")
                    else:
                        print(f"Borrowed books: {titles_borrowed_books}")
                        continue_process(
                            "  Would you like to view a new member’s [s]tatus or go-[b]ack to the previous menu?\n",
                            "s",
                            "b",
                            "Invalid selection please enter [s] to view a new member's status or [b] to go back to menu\n")

        else:
            print("No members in the library yet...Please add new members before checking status")
            continue_process("  Would you like to view a new member’s [s]tatus or go-[b]ack to the previous menu?\n",
                             "s",
                             "b",
                             "Invalid selection please enter [s] to view a new member's status or [b] to go back to menu\n")


def view_book_status():
    global array_list_book
    global is_empty_borrowing_members
    global add_flag
    add_flag = True
    borrowing_members = []
    is_empty_borrowing_members = True
    while add_flag:
        book_id = validate(f"Please enter a valid book ID :\n",
                           "A valid book ID must be a positive integer")
        if len(array_list_book) > 0:
            for book in array_list_book:
                if book.id == book_id:
                    print(f"Book[{book.id}]: {book.title}\n"
                          f"Available Number of copies:{book.number_of_copies}")
                    if len(book.member_borrowing) > 0:
                        is_empty_borrowing_members = False
                        for member in book.member_borrowing:
                            borrowing_members.append(member.name)
                    else:
                        is_empty_borrowing_members = True

            if is_empty_borrowing_members:
                print("List of Members borrowing: None")
                continue_process("Would you like to view a new book [s]tatus or go-[b]ack to the previous menu?\n",
                                 "s",
                                 "b",
                                 "Invalid selection please enter [s] to view book status or [b] to go back to menu\n")
            else:
                print(f"List of Members borrowing: {borrowing_members}")
                continue_process("Would you like to view a new book [s]tatus or go-[b]ack to the previous menu?\n",
                                 "s",
                                 "b",
                                 "Invalid selection please enter [s] to view book status or [b] to go back to menu\n")
        else:
            print("No books in the library yet...Please add new books before checking status")
            continue_process("Would you like to view a new book [s]tatus or go-[b]ack to the previous menu?\n",
                             "s",
                             "b",
                             "Invalid selection please enter [s] to view book status or [b] to go back to menu\n")


def main():
    global array_list_book
    global array_list_member
    array_list_book = []
    array_list_member = []
    welcome_banner()
    flag = True
    while flag:
        menu_options()
        selection = validate("Please select an option\n", "Invalid selection! A number between 1 and 7 was expected.")

        if selection == 1:
            print("---Adding a new member---")
            add_member()
        elif selection == 2:
            print("---Adding a new book---")
            add_book()
        elif selection == 3:
            print("---Processing borrowing---")
            process_borrowing()
        elif selection == 4:
            print("--Processing a return---")
            process_return()
        elif selection == 5:
            print("--Viewing member status---")
            view_member_status()
        elif selection == 6:
            print("Viewing book status---")
            view_book_status()
        elif selection == 7:
            print("Thanks for using the library System...\nGoodbye")
            flag = False
        else:
            print("Invalid selection! A number between 1 and 7 was expected.")


if __name__ == '__main__':
    main()
