# Secure Code Assessment
# Sample Login Application

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12345"


def login():
    print("===== User Login System =====")

    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login Successful!")
        print("Welcome to the application.")
    else:
        print("Invalid username or password.")


login()