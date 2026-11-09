import hashlib

# Store a hashed password instead of plain text
USERNAME = "admin"
PASSWORD = "12345"

hashed_password = hashlib.sha256(
    PASSWORD.encode()
).hexdigest()

attempts = 0
max_attempts = 3

print("===== Secure Login System =====")

while attempts < max_attempts:
    username = input("Enter username: ")
    password = input("Enter password: ")

    entered_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    if username == USERNAME and entered_hash == hashed_password:
        print("Login Successful!")
        print("Welcome to the application.")
        break
    else:
        attempts += 1
        print("Invalid username or password.")
        print("Attempts remaining:", max_attempts - attempts)

if attempts == max_attempts:
    print("Account temporarily locked.")