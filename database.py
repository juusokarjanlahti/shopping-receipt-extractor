import sqlite3

# Initialize database connection
conn = sqlite3.connect('receipts.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        total_cost REAL NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receipt_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER DEFAULT 1,
        deposit REAL DEFAULT 0.0,
        FOREIGN KEY (receipt_id) REFERENCES receipts (id)
    )
    ''')
    conn.commit()

def save_receipt(date, time, total_cost, items):
    cursor.execute(
        'INSERT INTO receipts (date, time, total_cost) VALUES (?, ?, ?)',
        (date, time, total_cost)
    )
    receipt_id = cursor.lastrowid
    for item in items:
        cursor.execute(
            'INSERT INTO items (receipt_id, item_name, price, quantity, deposit) VALUES (?, ?, ?, ?, ?)',
            (receipt_id, item['Item'], item['Price (EUR)'], item['Quantity'], item['Deposit (EUR)'])
        )
    conn.commit()

def get_receipts():
    cursor.execute('SELECT * FROM receipts')
    return cursor.fetchall()

def get_items_for_receipt(receipt_id):
    cursor.execute('SELECT * FROM items WHERE receipt_id = ?', (receipt_id,))
    return cursor.fetchall()
