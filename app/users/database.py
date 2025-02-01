import sqlite3
import hashlib

# Connect to the database
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
""")
conn.commit()

def insert_user(full_name, email, password):
    """Stores user data in the database with hashed password."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)", 
                       (full_name, email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Email already exists
    return True

def get_user(email, password):
    """Fetch user from database and verify password."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_password))
    return cursor.fetchone()
