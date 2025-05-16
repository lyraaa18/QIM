import tkinter as tk
from tkinter import ttk, messagebox, filedialog, StringVar
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2
import numpy as np
import datetime
import random
import os
from utils.watermark import embed_watermark
from utils.invoice_gen import InvoiceGenerator

class CreateInvoicePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.watermark_img = None
        self.invoice_img = None
        self.watermarked_img = None
        self.invoice_generator = InvoiceGenerator()
        
        self.selected_items = []
        self.item_entries = []
        
        self.create_widgets()
        
        self.load_default_watermark()
    
    def create_widgets(self):
        header = ttk.Frame(self, style="Primary.TFrame")
        header.pack(fill="x", pady=10)
        
        ttk.Label(
            header,
            text="Create Watermarked Invoice",
            font=("Helvetica", 18, "bold"),
            style="Primary.TLabel"
        ).pack(pady=10)
        
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        left_panel = ttk.LabelFrame(main_frame, text="Invoice Details", padding=10)
        left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        recipient_frame = ttk.Frame(left_panel)
        recipient_frame.pack(fill="x", pady=10)
        
        ttk.Label(recipient_frame, text="Recipient Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.recipient_var = StringVar()
        ttk.Entry(recipient_frame, textvariable=self.recipient_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        self.recipient_var.set("Client Name")
        
        self.item_select_frame = ttk.LabelFrame(left_panel, text="Select Items")
        self.item_select_frame.pack(fill="both", expand=True, pady=10)
        
        self.add_item_row()
        
        ttk.Button(
            self.item_select_frame,
            text="Add Another Item",
            command=self.add_item_row
        ).pack(pady=5)
        
        middle_panel = ttk.LabelFrame(main_frame, text="Watermark", padding=10)
        middle_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(
            middle_panel,
            text="Using default watermark.png"
        ).pack(pady=10)
        
        self.watermark_canvas = tk.Canvas(middle_panel, width=200, height=200, bg="#f0f0f0")
        self.watermark_canvas.pack(pady=10)
        
        ttk.Button(
            middle_panel,
            text="Generate Invoice",
            command=self.generate_watermarked_invoice,
            style="Accent.TButton"
        ).pack(pady=10)
        
        right_panel = ttk.LabelFrame(main_frame, text="Watermarked Result", padding=10)
        right_panel.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        ttk.Button(
            right_panel,
            text="Save Result",
            command=self.save_result
        ).pack(pady=5)
        
        self.result_canvas = tk.Canvas(right_panel, width=400, height=500, bg="#f0f0f0")
        self.result_canvas.pack(pady=10)
        
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
    
    def add_item_row(self):
        available_items = list(self.invoice_generator.get_available_items().keys())
        
        item_frame = ttk.Frame(self.item_select_frame)
        item_frame.pack(fill="x", pady=5)
        
        item_var = StringVar()
        qty_var = tk.IntVar()
        qty_var.set(1)
        
        if available_items:
            item_var.set(available_items[0])
        
        item_option = ttk.Combobox(
            item_frame,
            textvariable=item_var,
            values=available_items,
            width=25
        )
        item_option.grid(row=0, column=0, padx=5)
        
        ttk.Spinbox(
            item_frame,
            from_=1,
            to=100,
            width=5,
            textvariable=qty_var
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            item_frame,
            text="✕",
            width=2,
            command=lambda f=item_frame: self.remove_item_row(f)
        ).grid(row=0, column=2, padx=5)
        
        self.item_entries.append((item_frame, item_var, qty_var))
    
    def remove_item_row(self, frame):
        for i, (f, _, _) in enumerate(self.item_entries):
            if f == frame:
                self.item_entries.pop(i)
                frame.destroy()
                break
        
        if not self.item_entries:
            self.add_item_row()
    
    def generate_watermarked_invoice(self):
        if not self.generate_invoice():
            return False
        
        self.embed_watermark()
        return True
    
    def generate_invoice(self):
        recipient_name = self.recipient_var.get()
        
        selected_items = []
        for _, item_var, qty_var in self.item_entries:
            item_name = item_var.get()
            quantity = qty_var.get()
            selected_items.append((item_name, quantity))
        
        if not selected_items:
            messagebox.showwarning("Warning", "Please select at least one item")
            return False
        
        self.invoice_img = self.invoice_generator.generate(recipient_name, selected_items)
        return True
    
    def load_default_watermark(self):
        watermark_path = "watermark.png"
        if os.path.exists(watermark_path):
            self.watermark_img = cv2.imread(watermark_path)
            self.watermark_img = cv2.cvtColor(self.watermark_img, cv2.COLOR_BGR2RGB)
            self.display_image(self.watermark_img, self.watermark_canvas, (200, 200))
        else:
            self.create_default_watermark()
            messagebox.showinfo("Info", "Created default watermark because 'watermark.png' was not found")
    
    def create_default_watermark(self):
        img = np.ones((200, 200, 3), dtype=np.uint8) * 255
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, "PAID", (50, 100), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        self.watermark_img = img
        self.display_image(self.watermark_img, self.watermark_canvas, (200, 200))
        
        cv2.imwrite("watermark.png", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    
    def embed_watermark(self):
        if self.invoice_img is None:
            messagebox.showerror("Error", "Please generate an invoice first")
            return False
        if self.watermark_img is None:
            messagebox.showerror("Error", "Watermark image not available")
            return False
            
        self.watermarked_img = embed_watermark(self.invoice_img, self.watermark_img)
        self.display_image(self.watermarked_img, self.result_canvas, (400, 500))
        messagebox.showinfo("Success", "Watermarked invoice generated successfully")
        return True
    
    def save_result(self):
        if self.watermarked_img is None:
            messagebox.showerror("Error", "No watermarked image to save")
            return
        
        invoice_number = self.invoice_generator.last_invoice_number
        default_filename = f"{invoice_number}.png"
        
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.watermarked_img, cv2.COLOR_RGB2BGR))
            
            from utils.history_manager import add_to_history
            
            recipient = self.recipient_var.get()
            total_amount = sum(self.invoice_generator.available_items[item_var.get()] * qty_var.get() 
            for _, item_var, qty_var in self.item_entries)
            
            add_to_history(invoice_number, recipient, total_amount, file_path)
            messagebox.showinfo("Success", f"Image saved to {file_path}")
    
    def display_image(self, img, canvas, size):
        if img is None:
            return
            
        h, w = img.shape[:2]
        aspect_ratio = w / h
        
        if aspect_ratio > 1:
            new_w = size[0]
            new_h = int(size[0] / aspect_ratio)
        else:
            new_h = size[1]
            new_w = int(size[1] * aspect_ratio)
        
        display_img = cv2.resize(img.copy(), (new_w, new_h))
        
        pil_img = Image.fromarray(display_img)
        photo_img = ImageTk.PhotoImage(image=pil_img)
        
        canvas.config(width=new_w, height=new_h)
        canvas.create_image(new_w // 2, new_h // 2, image=photo_img, anchor=tk.CENTER)
        canvas.image = photo_img