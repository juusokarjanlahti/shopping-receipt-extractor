import tkinter as tk
import logging
from database import create_tables
from userinterface import ReceiptApp

"""
Main module for the Shopping Receipt Extractor application.
This module initializes the database tables and starts the GUI application.

Modules
-------
tkinter : Provides the GUI framework.
logging : Provides logging capabilities.
database : Contains the function to create database tables.
userinterface : Contains the ReceiptApp class for the GUI.

Functions
---------
main()
    Initializes the database tables and starts the GUI application.

Usage
-----
Run this module directly to start the application.
"""

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        # Initialize database tables
        create_tables()
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        exit(1)

    # Start the GUI application
    root = tk.Tk()
    app = ReceiptApp(root)
    root.mainloop()