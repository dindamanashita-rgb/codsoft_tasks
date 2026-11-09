# Secure Code Assessment
# Improved Login Application

import os
import hmac
import getpass

# Read credentials from environment variables
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def login():
    print("===== Secure User Login System =====")

    if not ADMIN_USERNAME or not ADMIN_PASSWORD:
        print("Application configuration is missing.")
        return

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    if (
        hmac.compare_digest(username, ADMIN_USERNAME)
        and hmac.compare_digest(password, ADMIN_PASSWORD)
    ):
        print("Login Successful!")
        print("Welcome to the application.")
    else:
        print("Invalid username or password.")


if __name__ == "__main__":
    login()