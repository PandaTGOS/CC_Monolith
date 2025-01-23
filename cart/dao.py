import json
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
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            contents TEXT,
            cost REAL
        )
    ''')
    conn.commit()


def parse_contents(contents: str) -> list:
    if not contents:
        return []
    try:
        return json.loads(contents)
    except json.JSONDecodeError:
        return []

def get_cart(username: str) -> dict:
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM carts WHERE username = ?', (username,))
    cart = cursor.fetchone()
    conn.close()
    return dict(cart) if cart else None


def add_to_cart(username: str, product_id: int):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    row = cursor.fetchone()
    contents = parse_contents(row['contents']) if row else []

    if product_id not in contents:
        contents.append(product_id)
    cursor.execute('INSERT OR REPLACE INTO carts (username, contents, cost) VALUES (?, ?, ?)',
                   (username, json.dumps(contents), 0))
    conn.commit()
    conn.close()

def remove_from_cart(username: str, product_id: int):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return

    contents = parse_contents(row['contents'])
    if product_id in contents:
        contents.remove(product_id)
    cursor.execute('INSERT OR REPLACE INTO carts (username, contents, cost) VALUES (?, ?, ?)',
                   (username, json.dumps(contents), 0))
    conn.commit()
    conn.close()


def delete_cart(username: str):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM carts WHERE username = ?', (username,))
    conn.commit()
