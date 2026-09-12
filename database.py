"""
database.py
------------
Handles all SQLite database operations for DDAS.
Stores metadata about every file that has been "downloaded" so we can
check future downloads against this history.
"""

import sqlite3
from datetime import datetime

DB_NAME = "ddas.db"


def create_table():
    """Creates the 'records' table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filehash TEXT NOT NULL,
            filesize INTEGER NOT NULL,
            username TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_record(filename, filehash, filesize, username, location):
    """Inserts a new download record into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO records (filename, filehash, filesize, username, timestamp, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (filename, filehash, filesize, username, timestamp, location))
    conn.commit()
    conn.close()


def check_duplicate(filehash):
    """
    Checks if a file with this hash already exists in the database.
    Returns the existing record (as a tuple) if found, else None.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT filename, username, timestamp, location
        FROM records
        WHERE filehash = ?
    """, (filehash,))
    result = cursor.fetchone()
    conn.close()
    return result


def get_all_records():
    """Returns all records currently stored in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_records_by_user(username):
    """
    Returns all records for a specific username.
    Used when the user wants to filter records instead of viewing all.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE username = ?", (username,))
    rows = cursor.fetchall()
    conn.close()
    return rows