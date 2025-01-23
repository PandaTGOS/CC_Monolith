import os.path
import sqlite3


def connect(path):
    exists = os.path.exists(path)
    __conn = sqlite3.connect(path)
    if not exists:
        create_tables(__conn)
    __conn.row_factory = sqlite3.Row
    return __conn


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()


def get_user(username: str) -> dict:
    conn = connect('auth.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username,  password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    return user


def add_user(username, password):
    conn = connect('auth.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()