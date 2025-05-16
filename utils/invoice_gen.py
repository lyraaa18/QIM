from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import datetime
import random
import locale

locale.setlocale(locale.LC_ALL, 'id_ID')

def format_rupiah(amount):
    return locale.currency(amount, grouping=True, symbol=True)

def generate_invoice(recipient_name="Client Name", items=None):
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    invoice_number = f"INV-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    
    draw.text((50, 50), "INVOICE", fill="black", font=font_large)
    draw.text((50, 90), f"No. Invoice: {invoice_number}", fill="black", font=font_medium)
    draw.text((50, 120), f"Tanggal: {datetime.datetime.now().strftime('%d-%m-%Y')}", fill="black", font=font_medium)
    
    draw.text((width-250, 50), "SealPay Furniture", fill="black", font=font_medium)
    draw.text((width-250, 80), "Jl. Merdeka No. 123", fill="black", font=font_small)
    draw.text((width-250, 100), "Tasikmalaya, Jawa Barat", fill="black", font=font_small)
    draw.text((width-250, 120), "Telp: (0265) 1234567", fill="black", font=font_small)
    
    draw.text((50, 160), "Kepada:", fill="black", font=font_medium)
    draw.text((50, 180), recipient_name, fill="black", font=font_small)
    
    if items is None or len(items) == 0:
        items = [
            ("Meja Makan Kayu Jati", 1, 2500000),
            ("Sofa 3 Seat", 2, 3500000),
            ("Lemari Pakaian 3 Pintu", 1, 1800000)
        ]

    y_pos = 230
    draw.text((60, y_pos), "Nama Barang", fill="black", font=font_medium)
    draw.text((350, y_pos), "Jumlah", fill="black", font=font_medium)
    draw.text((450, y_pos), "Harga Satuan", fill="black", font=font_medium)
    draw.text((600, y_pos), "Total", fill="black", font=font_medium)
    
    draw.line([(50, y_pos + 25), (width - 50, y_pos + 25)], fill="black", width=1)
    
    y_pos += 40
    total = 0
    
    for name, qty, price in items:
        amount = qty * price
        total += amount
        
        draw.text((60, y_pos), name, fill="black", font=font_small)
        draw.text((350, y_pos), str(qty), fill="black", font=font_small)
        draw.text((450, y_pos), format_rupiah(price), fill="black", font=font_small)
        draw.text((600, y_pos), format_rupiah(amount), fill="black", font=font_small)
        
        y_pos += 40
    
    draw.line([(400, y_pos + 10), (width - 50, y_pos + 10)], fill="black", width=1)
    
    draw.text((500, y_pos + 20), "TOTAL:", fill="black", font=font_medium)
    draw.text((600, y_pos + 20), format_rupiah(total), fill="black", font=font_medium)
    
    draw.text((50, y_pos + 80), "Pembayaran: Jatuh tempo 30 hari", fill="black", font=font_small)
    draw.text((50, y_pos + 100), "Terima kasih atas pembelian Anda!", fill="black", font=font_small)
    
    img_np = np.array(img)
    return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

class InvoiceGenerator:
    
    def __init__(self):
        self.available_items = {
            "Meja Makan Kayu Jati": 2500000,
            "Sofa 3 Seat": 3500000,
            "Lemari Pakaian 3 Pintu": 1800000,
            "Tempat Tidur King Size": 5000000,
            "Kursi Tamu": 1200000,
            "Meja Kerja Minimalis": 1500000,
            "Rak Buku Kayu": 800000,
            "Meja Rias": 2200000
        }
        self.last_invoice_number = ""
    
    def get_available_items(self):
        return self.available_items
    
    def generate(self, recipient_name, selected_items):
        items = []
        for item_name, quantity in selected_items:
            if item_name in self.available_items:
                price = self.available_items[item_name]
                items.append((item_name, quantity, price))
        
        invoice_img = generate_invoice(recipient_name, items)
        
        self.last_invoice_number = f"INV-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        return invoice_img