import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import os

class SmartMartBill:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Mart - Bill Receipt")
        self.root.configure(bg='white')
        self.items = []
        self.subtotal = 0.0
        self.tax = 0.0
        self.total = 0.0
        self.load_items()
        self.create_bill_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)

    def load_items(self):
        if os.path.exists("cart.json"):
            with open("cart.json", "r") as f:
                data = json.load(f)
                self.items = data.get("items", [])
            for item in self.items:
                self.subtotal += float(item["total_price"])
            self.tax = round(self.subtotal * 0.05, 2)
            self.total = round(self.subtotal + self.tax, 2)

    def create_bill_window(self):
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill='both', expand=True)

        self.create_header(main_frame)
        self.create_customer_info(main_frame)
        self.create_bill_content(main_frame)
        self.create_total_section(main_frame)
        self.create_footer(main_frame)

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg='#ecf0f1', pady=10)
        header_frame.pack(fill='x')

        tk.Label(header_frame, text="SMART MART", font=('Arial', 24, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack()
        tk.Label(header_frame, text="AI-Powered Smart Shopping", font=('Arial', 12), bg='#ecf0f1').pack()
        tk.Label(header_frame, text="Address: 123 Tech Street, Smart City", font=('Arial', 10), bg='#ecf0f1').pack()
        tk.Label(header_frame, text="Phone: +91-1234567890", font=('Arial', 10), bg='#ecf0f1').pack()

    def create_customer_info(self, parent):
        info_frame = tk.Frame(parent, bg='white')
        info_frame.pack(fill='x', padx=20, pady=(10, 0))

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        bill_no = "SM" + datetime.now().strftime("%Y%m%d%H%M%S")

        tk.Label(info_frame, text=f"Bill No: {bill_no}", bg='white', font=('Arial', 10)).pack(anchor='w')
        tk.Label(info_frame, text=f"Date: {now}", bg='white', font=('Arial', 10)).pack(anchor='w')
        tk.Label(info_frame, text="Cashier: AI Assistant", bg='white', font=('Arial', 10)).pack(anchor='w')

    def create_bill_content(self, parent):
        content_frame = tk.Frame(parent, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=(10, 0))

        header_frame = tk.Frame(content_frame, bg='#ecf0f1', relief='solid', bd=1)
        header_frame.pack(fill='x', pady=(0, 5))

        for text, width in [("Item", 20), ("Weight", 10), ("Rate/Kg", 10), ("Amount", 10)]:
            tk.Label(header_frame, text=text, font=('Arial', 12, 'bold'), bg='#ecf0f1', width=width, anchor='w').pack(side='left', padx=6, pady=6)

        canvas = tk.Canvas(content_frame, bg='white', height=200)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for item in self.items:
            name = item.get("name", "")
            weight = f"{item.get('weight_grams', 0)}g"
            rate = f"₹{item.get('price_per_kg', 0)}"
            amount = f"₹{item.get('total_price', 0):.2f}"
            self.insert_item(name, weight, rate, amount)

    def insert_item(self, name, weight, rate, amount):
        item_frame = tk.Frame(self.scrollable_frame, bg='white', highlightbackground="black", highlightthickness=1)
        item_frame.pack(fill='x', pady=2)

        for text, width in [(name, 20), (weight, 10), (rate, 10), (amount, 10)]:
            tk.Label(item_frame, text=text, font=('Arial', 12), bg='white', width=width, anchor='w').pack(side='left', padx=6, pady=4)

    def create_total_section(self, parent):
        total_frame = tk.Frame(parent, bg='white')
        total_frame.pack(fill='x', padx=20, pady=(0, 10))

        tk.Label(total_frame, text="─" * 90, bg='white', fg='#bdc3c7').pack()

        totals_frame = tk.Frame(total_frame, bg='white')
        totals_frame.pack(anchor='e')

        self.subtotal_label = tk.Label(totals_frame, text=f"Subtotal: ₹{self.subtotal:.2f}", font=('Arial', 14, 'bold'), bg='white', fg='#2c3e50')
        self.subtotal_label.pack(anchor='e', pady=2)

        self.tax_label = tk.Label(totals_frame, text=f"Tax (5%): ₹{self.tax:.2f}", font=('Arial', 14, 'bold'), bg='white', fg='#2c3e50')
        self.tax_label.pack(anchor='e', pady=2)

        tk.Label(totals_frame, text="─" * 40, bg='white', fg='#bdc3c7').pack(anchor='e', pady=4)

        self.total_label = tk.Label(totals_frame, text=f"TOTAL: ₹{self.total:.2f}", font=('Arial', 18, 'bold'), bg='white', fg='#27ae60')
        self.total_label.pack(anchor='e', pady=4)

        tk.Label(total_frame, text="🙏 Thank you for shopping with Smart Mart!\nHave a healthy day! 🌟", font=('Arial', 12, 'italic'), bg='white', fg='#7f8c8d', justify='center').pack(pady=10)

    def create_footer(self, parent):
        footer_frame = tk.Frame(parent, bg='#ecf0f1', pady=10)
        footer_frame.pack(fill='x')

        tk.Button(footer_frame, text="Print", font=('Arial', 12), width=10).pack(side='left', padx=20)
        tk.Button(footer_frame, text="Clear", font=('Arial', 12), width=10).pack(side='left')
        tk.Button(footer_frame, text="Quit", font=('Arial', 12), width=10, command=self.on_quit).pack(side='right', padx=20)

    def on_quit(self):
        if os.path.exists("cart.json"):
            os.remove("cart.json")
        self.root.destroy()


def show_bill():
    root = tk.Tk()
    root.geometry("700x800")
    app = SmartMartBill(root)
    root.mainloop()

if __name__ == "__main__":
    show_bill()
