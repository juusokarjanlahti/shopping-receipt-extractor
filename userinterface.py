import csv
from tkinter import Toplevel, Label, Button, filedialog, ttk, messagebox
from database import save_receipt, get_receipts, get_items_for_receipt, delete_receipt
from process import perform_ocr, process_extracted_text

class ReceiptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Receipt Processor")
        self.root.geometry("800x600")

        self.upload_btn = Button(self.root, text="Upload Receipt", command=self.upload_receipt)
        self.upload_btn.pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Date", "Time", "Total"), show="headings")
        self.tree.heading("ID", text="Receipt ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Total", text="Total Cost (EUR)")
        self.tree.pack(fill="both", expand=True, pady=20)

        self.view_items_btn = Button(self.root, text="View Items", command=self.view_items)
        self.view_items_btn.pack(pady=5)

        self.export_btn = Button(self.root, text="Export to CSV", command=self.export_to_csv)
        self.export_btn.pack(pady=5)

        self.refresh_btn = Button(self.root, text="Refresh Data", command=self.load_receipts)
        self.refresh_btn.pack(pady=10)

        self.delete_btn = Button(self.root, text="Delete Receipt", command=self.delete_receipt)
        self.delete_btn.pack(pady=5)

        self.load_receipts()

    def upload_receipt(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if not file_path:
            return

        try:
            extracted_text = perform_ocr(file_path)
            date, time, total, items = process_extracted_text(extracted_text)
            save_receipt(date, time, total, items)
            messagebox.showinfo("Success", "Receipt processed and saved!")
            self.load_receipts()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process receipt: {e}")

    def load_receipts(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            receipts = get_receipts()
            for receipt in receipts:
                self.tree.insert('', 'end', values=receipt)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load receipts: {e}")

    def view_items(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showinfo("No selection", "Please select a receipt to view its items.")
            return

        receipt_id = self.tree.item(selected_item, "values")[0]
        items = get_items_for_receipt(receipt_id)

        popup = Toplevel(self.root)
        popup.title("Receipt Items")
        popup.geometry("600x400")

        tree = ttk.Treeview(popup, columns=("Item", "Price", "Quantity", "Deposit", "EUR/kg"), show="headings")
        tree.heading("Item", text="Item Name")
        tree.heading("Price", text="Price (EUR)")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Deposit", text="Deposit (EUR)")
        tree.heading("EUR/kg", text="Price per kg (EUR)")
        tree.pack(fill="both", expand=True, pady=20)

        for item in items:
            formatted_price = format(float(item[3]), '.2f')
            formatted_deposit = format(float(item[5]), '.2f') if item[5] is not None else None
            formatted_price_per_kg = format(float(item[6]), '.2f') if item[6] is not None else None
            tree.insert('', 'end', values=(item[2], formatted_price, item[4], formatted_deposit, formatted_price_per_kg))

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            receipts = get_receipts()
            with open(file_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["ID", "Date", "Time", "Total Cost (EUR)"])
                writer.writerows(receipts)
            messagebox.showinfo("Success", "Data exported to CSV successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")

    def delete_receipt(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No receipt selected!")
            return

        try:
            for selected_item in selected_items:
                receipt_id = self.tree.item(selected_item, 'values')[0]
                delete_receipt(receipt_id)
            messagebox.showinfo("Success", "Selected receipts deleted successfully!")
            self.load_receipts()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete receipts: {e}")