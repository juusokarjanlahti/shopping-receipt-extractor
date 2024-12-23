# Shopping Receipt Extractor

This project is a shopping receipt extractor that 
- processes receipts,
- extracts items and prices using OCR (Optical Character Recognition),
- stores the data in a SQLite database.

The application also provides a minimal user interface to view and export the extracted data.

## Prerequisites

- Python 3.x
- [`pillow`](https://github.com/python-pillow/Pillow) PNG to image 
- [`pytesseract`](https://github.com/h/pytesseract) image to string 
- `tkinter` GUI
- `sqlite3` DB

## Project Structure

- `main.py`: The main entry point of the application. Initializes the database and starts the GUI.
- `database.py`: Contains functions to create tables, save receipts, and retrieve data from the SQLite database.
- `process.py`: Contains functions to perform OCR on receipt images and process the extracted text.
- `userinterface.py`: Contains the GUI implementation using `tkinter`.


## Usage
1. Clone the repository:

```sh
git clone https://github.com/yourusername/shopping-receipt-extractor.git
cd shopping-receipt-extractor
```

2. Run the application:

```sh
python main.py
```

3. Use the GUI to upload receipt images, view extracted data, and export data to CSV.

You can use the cropped example `receipt.png` for testing.
