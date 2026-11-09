from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from encryption import encrypt_file, decrypt_file
import sqlite3
import os
import uuid
import io

app = Flask(__name__)
app.secret_key = "change-this-secret-before-deployment"

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

os.makedirs("uploads", exist_ok=True)

DATABASE = "database.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            stored_name TEXT NOT NULL,
            owner_id INTEGER NOT NULL,
            FOREIGN KEY(owner_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    files = conn.execute(
        "SELECT * FROM files WHERE owner_id = ?",
        (session["user_id"],)
    ).fetchall()

    conn.close()

    return render_template("index.html", files=files)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or len(password) < 8:
            flash("Enter a username and password of at least 8 characters.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
            flash("Registration successful!")

        except sqlite3.IntegrityError:
            flash("Username already exists.")

        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("home"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/upload", methods=["POST"])
def upload():
    if "user_id" not in session:
        return redirect(url_for("login"))

    uploaded_file = request.files.get("file")

    if not uploaded_file or not uploaded_file.filename:
        flash("Please select a file.")
        return redirect(url_for("home"))

    filename = secure_filename(uploaded_file.filename)
    file_data = uploaded_file.read()

    if not filename or not file_data:
        flash("Invalid or empty file.")
        return redirect(url_for("home"))

    encrypted_data = encrypt_file(file_data)
    stored_name = str(uuid.uuid4()) + ".enc"

    path = os.path.join("uploads", stored_name)

    with open(path, "wb") as f:
        f.write(encrypted_data)

    conn = get_db()

    conn.execute(
        "INSERT INTO files (filename, stored_name, owner_id) VALUES (?, ?, ?)",
        (filename, stored_name, session["user_id"])
    )

    conn.commit()
    conn.close()

    flash("File uploaded and encrypted successfully!")
    return redirect(url_for("home"))


@app.route("/download/<int:file_id>")
def download(file_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    file = conn.execute(
        "SELECT * FROM files WHERE id = ? AND owner_id = ?",
        (file_id, session["user_id"])
    ).fetchone()

    conn.close()

    if not file:
        return "File not found or access denied", 404

    path = os.path.join("uploads", file["stored_name"])

    if not os.path.exists(path):
        return "File not found", 404

    with open(path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_file(encrypted_data)

    return send_file(
        io.BytesIO(decrypted_data),
        as_attachment=True,
        download_name=file["filename"]
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)