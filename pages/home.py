import tkinter as tk
from tkinter import ttk

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        style = ttk.Style()
        style.configure("Card.TFrame", 
        borderwidth=2,
        relief="solid",
        padding=10)
        style.configure("Card.TLabel", 
        font=('Helvetica', 10),
        padding=5)
        
        header = ttk.Frame(self, style="Primary.TFrame")
        header.pack(fill="x", pady=(0, 20))
        
        ttk.Label(
            header,
            text="Qimchi - Invoice Watermarking System",
            font=("Helvetica", 24, "bold"),
            style="Primary.TLabel"
        ).pack(pady=20)
        
        content = ttk.Frame(self)
        content.pack(fill="both", expand=True, padx=50, pady=20)
        
        features = [
            {
                "title": "Create Watermarked Invoice",
                "desc": "Generate invoices with embedded digital watermarks",
                "action": lambda: self.controller.show_page("CreateInvoicePage")
            },
            {
                "title": "Verify Invoice Authenticity",
                "desc": "Check if an invoice has been tampered with by extracting its watermark",
                "action": lambda: self.controller.show_page("VerifyInvoicePage")
            }
        ]
        
        for i, feature in enumerate(features):
            card = ttk.Frame(content, style="Card.TFrame")
            card.grid(row=0, column=i, padx=20, pady=10, sticky="nsew")
            
            ttk.Label(
                card,
                text=feature["title"],
                font=("Helvetica", 14, "bold"),
                style="Card.TLabel"
            ).pack(pady=10, padx=20, anchor="w")
            
            ttk.Label(
                card,
                text=feature["desc"],
                style="Card.TLabel"
            ).pack(pady=5, padx=20, anchor="w")
            
            ttk.Button(
                card,
                text="Go →",
                command=feature["action"],
                style="Accent.TButton"
            ).pack(pady=20, padx=20, anchor="e")
            
            content.grid_columnconfigure(i, weight=1)
        
        content.grid_rowconfigure(0, weight=1)