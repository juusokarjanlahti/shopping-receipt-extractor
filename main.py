from userinterface import ReceiptApp
from database import create_tables
import tkinter as tk
import csv

if __name__ == "__main__":
    try:
        # Initialize database tables
        create_tables()
    except Exception as e:
        print(f"Error initializing database: {e}")
        exit(1)

    # Start the application
    root = tk.Tk()
    app = ReceiptApp(root)
    root.mainloop()