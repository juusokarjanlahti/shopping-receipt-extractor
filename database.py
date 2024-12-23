import sqlite3

def get_db_connection():
    """
    Get a database connection.

    Returns:
    sqlite3.Connection: A connection object to the SQLite database.
    """
    conn = sqlite3.connect('receipts.db')
    return conn

def create_tables():
    """
    Initialize the database by creating the necessary tables.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
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
            quantity REAL DEFAULT 1,
            deposit REAL DEFAULT 0.0,
            price_per_kg REAL DEFAULT NULL,
            FOREIGN KEY (receipt_id) REFERENCES receipts (id)
        )
        ''')
        conn.commit()

def save_receipt(date, time, total, items):
    """
    Save a receipt and its items to the database.

    Parameters:
    date (str): The date of the receipt.
    time (str): The time of the receipt.
    total (float): The total cost of the receipt.
    items (list of dict): A list of items in the receipt.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO receipts (date, time, total_cost)
        VALUES (?, ?, ?)
        ''', (date, time, total))
        receipt_id = cursor.lastrowid

        for item in items:
            cursor.execute('''
            INSERT INTO items (receipt_id, item_name, price, quantity, deposit, price_per_kg)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (receipt_id, item["Item"], item["Price (EUR)"], item["Quantity"], item["Deposit (EUR)"], item["Price per kg (EUR/kg)"]))

        conn.commit()

def get_receipts():
    """
    Retrieve all receipts from the database.

    Returns:
    list: A list of receipts.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM receipts')
        return cursor.fetchall()

def get_items_for_receipt(receipt_id):
    """
    Retrieve items for a specific receipt from the database.

    Parameters:
    receipt_id (int): The ID of the receipt.

    Returns:
    list: A list of items for the receipt.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, receipt_id, item_name, price, quantity, deposit, price_per_kg FROM items WHERE receipt_id = ?', (receipt_id,))
        return cursor.fetchall()

def delete_receipt(receipt_id):
    """
    Delete a receipt and its items from the database.

    Parameters:
    receipt_id (int): The ID of the receipt to delete.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE receipt_id = ?', (receipt_id,))
        cursor.execute('DELETE FROM receipts WHERE id = ?', (receipt_id,))
        conn.commit()