import re
import logging
from PIL import Image
import pytesseract

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def perform_ocr(file_path):
    try:
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image, lang="fin")
        logging.info("Raw extracted text:\n%s", extracted_text)  # Log the raw extracted text
        return extracted_text
    except Exception as e:
        raise RuntimeError(f"Error during OCR processing: {e}")

def process_extracted_text(extracted_text):
    """
    Process the extracted text to retrieve transaction details.

    Args:
        extracted_text (str): The raw text extracted from the receipt.

    Returns:
        tuple: A tuple containing:
            - transaction_date (str or None): The date of the transaction in the format 'dd/mm/yyyy'.
            - transaction_time (str or None): The time of the transaction in the format 'hh:mm'.
            - total_cost (float): The total cost of the transaction.
            - items (list of dict): A list of dictionaries, each containing:
                - 'Item' (str): The name of the item.
                - 'Price (EUR)' (float): The price of the item.
                - 'Quantity' (int): The quantity of the item.
                - 'Deposit (EUR)' (float): The deposit for the item.
    """
    # Initialize data
    transaction_date, transaction_time, total_cost = None, None, 0.0
    items = []

    # Extract date and time
    date_time_match = re.search(r"(\d{2}/\d{2}/\d{4})\s(\d{2}:\d{2})", extracted_text)
    if date_time_match:
        transaction_date = date_time_match.group(1)
        transaction_time = date_time_match.group(2)

    # Extract total cost
    total_cost_match = re.search(r"YHTEENSÄ EUR ([\d\.]+)", extracted_text, re.IGNORECASE)
    if total_cost_match:
        total_cost = float(total_cost_match.group(1).replace(',', '.'))

    # Extract items
    items_section = re.search(r"EUR(.*)Yhteensä", extracted_text, re.DOTALL)
    if items_section:
        items_text = items_section.group(1).strip()
        lines = items_text.splitlines()
        previous_item = None
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            logging.info("Processing line: %s", line)  # Log each line being processed

            # Check if the line contains quantity and price information for the previous item
            quantity_match = re.match(r"(\d+)\s*x\s*([\d,.,]+)", line)
            if quantity_match and previous_item:
                quantity = int(quantity_match.group(1))
                price = float(quantity_match.group(2).replace(',', '.'))
                previous_item["Price (EUR)"] = price
                previous_item["Quantity"] = quantity
                continue  # Skip adding this line as a new item

            # Check if the line contains item name and price
            item_match = re.match(r"(.+?)\s+([\d,\.]+)\s?[A-Z]?$", line)
            if item_match:
                item_name = item_match.group(1).strip()
                price = float(item_match.group(2).replace(',', '.'))
                quantity = 1

                previous_item = {"Item": item_name, "Price (EUR)": price, "Quantity": quantity, "Deposit (EUR)": 0.0}
                items.append(previous_item)

            # Handle deposits (Pantti)
            if "Pantti" in line:
                deposit_match = re.search(r"Pantti.*([\d,.,]+)", line)
                if deposit_match:
                    deposit = float(deposit_match.group(1).replace(',', '.'))
                    if items:
                        items[-1]["Deposit (EUR)"] = deposit  # Update the last item's deposit

    return transaction_date, transaction_time, total_cost, items
