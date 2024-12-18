
import pickle
from datetime import datetime, timedelta

class Birthday:
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Name:
    def __init__(self, value):
        self.value = value

class Phone:
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        self.value = value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Old phone number not found.")

    def add_birthday(self, date):
        self.birthday = Birthday(date)

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find(self, name):
        for record in self.records:
            if record.name.value == name:
                return record
        return None

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_birthdays = []
        for record in self.records:
            if record.birthday:
                birthday_date = record.birthday.value
                if today <= birthday_date <= today + timedelta(days=7):
                    if birthday_date.weekday() in [5, 6]:
                        birthday_date += timedelta(days=(7 - birthday_date.weekday()))
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": birthday_date.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return wrapper

@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(date)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record is None or record.birthday is None:
        return "Birthday not found."
    return f"Birthday: {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args, book):
    return book.get_upcoming_birthdays()

def parse_input(user_input):
    return user_input.split()

def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            name, phone = args
            record = book.find(name)
            message = "Contact updated."
            if record is None:
                record = Record(name)
                book.add_record(record)
                message = "Contact added."
            if phone:
                record.add_phone(phone)
            print(message)

        elif command == "change":
            name, old_phone, new_phone = args
            record = book.find(name)
            if record:
                record.change_phone(old_phone, new_phone)
                print("Phone number updated.")
            else:
                print("Contact not found.")

        elif command == "phone":
            name = args[0]
            record = book.find(name)
            if record:
                print(f"Phones: {', '.join(phone.value for phone in record.phones)}")
            else:
                print("Contact not found.")

        elif command == "all":
            for record in book.records:
                phones = ', '.join(phone.value for phone in record.phones) if record.phones else "No phones"
                birthday = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "No birthday"
                print(f"Name: {record.name.value}, Phones: {phones}, Birthday: {birthday}")

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            upcoming_birthdays = birthdays(args, book)
            if upcoming_birthdays:
                for entry in upcoming_birthdays:
                    print(f"Name: {entry['name']}, Birthday: {entry['birthday']}")
            else:
                print("No upcoming birthdays.")

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
