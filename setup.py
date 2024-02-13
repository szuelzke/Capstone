import sqlite3
import hashlib

conn = sqlite3.connect('FlashFin_main.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table for login information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')