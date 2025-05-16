import tkinter as tk
from tkinter import ttk, messagebox
import os
from utils.history_manager import get_history, open_invoice
from PIL import Image, ImageTk
import cv2
import numpy as np

class HistoryPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        
    def create_widgets(self):
        header = ttk.Frame(self, style="Primary.TFrame")
        header.pack(fill="x", pady=10)
        
        ttk.Label(
            header,
            text="Invoice History",
            font=("Helvetica", 18, "bold"),
            style="Primary.TLabel"
        ).pack(pady=10)
        
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.create_history_table(main_frame)
        
        refresh_frame = ttk.Frame(main_frame)
        refresh_frame.pack(fill="x", pady=10)
        
        ttk.Button(
            refresh_frame,
            text="Refresh History",
            command=self.refresh_history
        ).pack(side="right")
        
    def create_history_table(self, parent):
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("invoice_number", "recipient", "total_amount", "date_created")
        self.history_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.history_tree.heading("invoice_number", text="Invoice #")
        self.history_tree.heading("recipient", text="Recipient")
        self.history_tree.heading("total_amount", text="Amount")
        self.history_tree.heading("date_created", text="Date Created")
        
        self.history_tree.column("invoice_number", width=150)
        self.history_tree.column("recipient", width=200)
        self.history_tree.column("total_amount", width=100)
        self.history_tree.column("date_created", width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.history_tree.bind("<Double-1>", self.on_item_double_click)
        
        preview_frame = ttk.LabelFrame(parent, text="Invoice Preview")
        preview_frame.pack(fill="both", expand=True, pady=10)
        
        self.preview_canvas = tk.Canvas(preview_frame, width=400, height=300, bg="#f0f0f0")
        self.preview_canvas.pack(pady=10)
        
        self.history_tree.bind("<<TreeviewSelect>>", self.on_item_select)
        
        self.load_history_data()
        
    def load_history_data(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        history = get_history()
        
        for entry in history:
            self.history_tree.insert("", "end", values=(
                entry["invoice_number"],
                entry["recipient"],
                f"Rp. {entry['total_amount']:.2f}",
                entry["date_created"]
            ), tags=(entry["file_path"],))
            
    def on_item_double_click(self, event):
        selected_item = self.history_tree.selection()[0]
        file_path = self.history_tree.item(selected_item, "tags")[0]
        
        if not open_invoice(file_path):
            messagebox.showerror("Error", f"Could not open file: {file_path}")
            
    def on_item_select(self, event):
        selected_items = self.history_tree.selection()
        if not selected_items:
            return
            
        selected_item = selected_items[0]
        file_path = self.history_tree.item(selected_item, "tags")[0]
        
        self.show_preview(file_path)
        
    def show_preview(self, file_path):
        if not os.path.exists(file_path):
            self.preview_canvas.delete("all")
            self.preview_canvas.create_text(
                200, 150,
                text="File not found",
                font=("Helvetica", 14),
                fill="red"
            )
            return
            
        try:
            img = cv2.imread(file_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            h, w = img.shape[:2]
            aspect_ratio = w / h
            
            if aspect_ratio > 4/3:
                new_w = 400
                new_h = int(400 / aspect_ratio)
            else:
                new_h = 300
                new_w = int(300 * aspect_ratio)
                
            img_resized = cv2.resize(img, (new_w, new_h))
            
            pil_img = Image.fromarray(img_resized)
            photo_img = ImageTk.PhotoImage(image=pil_img)
            
            self.preview_canvas.delete("all")
            self.preview_canvas.config(width=new_w, height=new_h)
            self.preview_canvas.create_image(new_w // 2, new_h // 2, image=photo_img, anchor=tk.CENTER)
            self.preview_canvas.image = photo_img
            
        except Exception as e:
            self.preview_canvas.delete("all")
            self.preview_canvas.create_text(
                200, 150,
                text=f"Error loading preview: {str(e)}",
                font=("Helvetica", 12),
                fill="red"
            )
            
    def refresh_history(self):
        self.load_history_data()
        messagebox.showinfo("Success", "History refreshed successfully")
        
    def on_show_frame(self):
        self.load_history_data()