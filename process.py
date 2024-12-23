import re

def perform_ocr(file_path):
    # Implement OCR logic here using pytesseract or another OCR library
    from PIL import Image
    import pytesseract

    try:
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image, lang="fin")
        print("Raw extracted text:\n", extracted_text)  # Print the raw extracted text
        return extracted_text
    except Exception as e:
        raise RuntimeError(f"Error during OCR processing: {e}")

def process_extracted_text(extracted_text):
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
        for line in lines:
            item_match = re.match(r"(.+?)\s([\d,\.]+)\s?[A-Z]?", line)
            if item_match:
                item_name = item_match.group(1).strip()
                combined_price = float(item_match.group(2).replace(',', '.'))
                quantity = 1
                price = combined_price

                # Check for quantity and individual price
                quantity_match = re.search(r"(\d+)\s*x\s*([\d,\.]+)", line)
                if quantity_match:
                    quantity = int(quantity_match.group(1))
                    price = float(quantity_match.group(2).replace(',', '.'))

                items.append({"Item": item_name, "Price (EUR)": price, "Quantity": quantity, "Deposit (EUR)": 0.0})

            # Handle deposits (Pantti)
            if "Pantti" in line:
                deposit_match = re.search(r"Pantti.*([\d,\.]+)", line)
                if deposit_match:
                    deposit = float(deposit_match.group(1).replace(',', '.'))
                    if items:
                        items[-1]["Deposit (EUR)"] = deposit  # Update the last item's deposit

    return transaction_date, transaction_time, total_cost, items
