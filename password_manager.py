import getpass
import json
import os
import bcrypt

# Generate a hashed password from the user's input
def generate_hashed_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

# Check if the provided password matches the stored hashed password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

# Load users and hashed passwords from a JSON file
def load_users(file_path):
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as file:
        users = json.load(file)

    return users

# Save users and hashed passwords to a JSON file
def save_users(users, file_path):
    with open(file_path, "w") as file:
        json.dump(users, file)

def password_manager(username, passwords, passwords_file_path, key):
    while True:
        print("\n=== Password Manager ===")
        print("1. Save a password")
        print("2. Get a password")
        print("3. Logout")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            account = input("Enter the account name: ")
            password = getpass.getpass("Enter the password: ")
            passwords[account] = password
            save_passwords(passwords, passwords_file_path, key)

        elif choice == "2":
            account = input("Enter the account name: ")
            if account in passwords:
                password = passwords[account]
                print("Password:", password)
            else:
                print("Account not found!")

        elif choice == "3":
            print(f"Goodbye, {username}!")
            break

        else:
            print("Invalid choice. Please try again.")

def main():
    # Passwords file path
    passwords_file_path = "passwords.json"

    # Load existing users (if any)
    users = load_users(passwords_file_path)

    while True:
        print("\n=== Password Manager ===")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            username = input("Enter your username: ")
            if username in users:
                password = getpass.getpass("Enter your password: ")
                if verify_password(users[username], password):
                    print(f"Welcome, {username}!")
                    # Call the password manager function for logged-in users
                    password_manager(username, load_passwords(passwords_file_path, load_key("password_manager.key")), passwords_file_path, load_key("password_manager.key"))
                else:
                    print("Invalid username or password. Please try again.")
            else:
                print("User not found. Please sign up.")

        elif choice == "2":
            username = input("Enter your desired username: ")
            if username in users:
                print("Username already exists. Please choose a different username.")
            else:
                password = getpass.getpass("Enter your password: ")
                hashed_password = generate_hashed_password(password)
                users[username] = hashed_password
                save_users(users, passwords_file_path)
                print("Sign up successful! You can now log in.")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
