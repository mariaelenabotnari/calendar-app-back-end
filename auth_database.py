# auth_database.py
import sqlite3
import os

# Define the path to the authentication database
current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'UserAuth.db')

# Function to initialize the authentication database and create the 'users' table
def init_auth_db():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create 'users' table with predefined users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Pre-populated user data without hashed passwords
    users = [
        ('user1@example.com', 'password1'),
        ('user2@example.com', 'password2'),
        ('user3@example.com', 'password3'),
        ('xyz@gmail.com', 'faf232')
    ]

    # Insert predefined users if they don’t already exist
    cursor.executemany('INSERT OR IGNORE INTO users (email, password) VALUES (?, ?)', users)

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Function to verify user login credentials (plain-text comparison)
def verify_user(email, password):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return False

    # Compare password directly (no hashing)
    return user[0] == password

# Initialize the database with predefined users when the module is run directly
if __name__ == "__main__":
    init_auth_db()
