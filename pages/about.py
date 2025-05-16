import tkinter as tk
from tkinter import ttk

class AboutPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.create_widgets()
    
    def create_widgets(self):
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = ttk.Frame(main_container, style="Primary.TFrame")
        header.pack(fill="x", pady=(0, 20))
        
        ttk.Label(
            header,
            text="About SealPay",
            font=("Segoe UI", 28, "bold"),
            style="Primary.TLabel",
            foreground="#2c3e50"
        ).pack(pady=20)
        
        content = ttk.Frame(
            main_container,
            style="Card.TFrame",
            padding=(30, 20)
        )
        content.pack(fill="both", expand=True)
        
        about_text = """
SealPay (Quantum Index Modulation Digital Invoice) v1.2

A cutting-edge application for secure document authentication and protection 
using advanced digital watermarking technology.

© 2025 Quantum Security Solutions. All rights reserved.
        """
        
        ttk.Label(
            content,
            text=about_text,
            justify=tk.LEFT,
            font=("Segoe UI", 11),
            style="Card.TLabel",
            foreground="#34495e"
        ).pack(pady=10, padx=10, anchor="w")
        
        dev_frame = ttk.Frame(
            content,
            style="Card.TFrame",
            padding=(20, 15)
        )
        dev_frame.pack(fill="x", pady=(30, 10))
        
        ttk.Label(
            dev_frame,
            text="Development Team",
            font=("Segoe UI", 14, "bold"),
            style="Card.TLabel",
            foreground="#2c3e50"
        ).pack(anchor="w", pady=(0, 10))
        
        developers = [
            {"name": "Ikhwan Kurniawan Julianto", "npm": "237006102"},
            {"name": "Delvina Salma Hidayah", "npm": "237006103" },
            {"name": "Alya Shaumi", "npm": "237006109" },
        ]
        
        for dev in developers:
            dev_info = f"{dev['name']} ({dev['npm']})"
            ttk.Label(
                dev_frame,
                text=dev_info,
                font=("Segoe UI", 10),
                style="Card.TLabel",
                foreground="#7f8c8d"
            ).pack(anchor="w", padx=10, pady=2)
        
        ttk.Label(
            content,
            text="SealPay v1.2 | Build 2025.12.1",
            font=("Segoe UI", 8),
            style="Card.TLabel",
            foreground="#95a5a6"
        ).pack(side=tk.RIGHT, anchor="se", pady=(20, 0))