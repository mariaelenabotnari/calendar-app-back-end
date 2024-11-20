import sqlite3

# Connect to the database
conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()

# Create the 'favorites' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(event_id) REFERENCES events(id)
);
''')

conn.commit()
conn.close()
