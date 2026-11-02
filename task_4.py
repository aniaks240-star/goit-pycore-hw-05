from functools import wraps


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as error:
            return str(error) or "Give me name and phone please."
        except IndexError:
            return "Enter user name."
    return inner


def parse_input(user_input):
    parts = user_input.split()
    if not parts:
        return "", []
    return parts[0].casefold(), [part.casefold() for part in parts[1:]]


@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    contacts[name.casefold()] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
    name = name.casefold()
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    name = args[0].casefold()
    if len(args) != 1:
        raise ValueError("Enter one user name.")
    return contacts[name]


@input_error
def show_all(args, contacts):
    if args:
        raise ValueError("This command takes no arguments.")
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items()) or "No contacts."


@input_error
def say_hello(args, contacts):
    if args:
        raise ValueError("This command takes no arguments.")
    return "How can I help you?"


def main():
    contacts = {}
    handlers = {"add": add_contact, "change": change_contact,
                "phone": show_phone, "all": show_all, "hello": say_hello}
    print("Welcome to the assistant bot!")
    while True:
        try:
            command, args = parse_input(input("Enter a command: "))
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
            break
        if command in ("close", "exit") and not args:
            print("Good bye!")
            break
        if command in handlers:
            print(handlers[command](args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
