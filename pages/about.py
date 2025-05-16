import tkinter as tk
from tkinter import ttk

class AboutPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.create_widgets()
    
    def create_widgets(self):
        header = ttk.Frame(self, style="Primary.TFrame")
        header.pack(fill="x", pady=20)
        
        ttk.Label(
            header,
            text="About Invoice Watermarking System",
            font=("Helvetica", 24, "bold"),
            style="Primary.TLabel"
        ).pack(pady=20)
        
        content = ttk.Frame(self)
        content.pack(fill="both", expand=True, padx=50, pady=20)
        
        about_text = """
        Invoice Watermarking System v1.0
        
        This application provides a secure way to:
        - Generate professional invoices
        - Embed invisible digital watermarks
        - Verify invoice authenticity
        
        Features:
        • Quantum Index Modulation watermarking
        • Tamper detection
        • Multi-channel watermark extraction
        • Modern user interface
        
        Developed using:
        - Python 3
        - OpenCV for image processing
        - Tkinter for GUI
        
        © 2023 Watermarking Technologies
        """
        
        ttk.Label(
            content,
            text=about_text,
            justify=tk.LEFT,
            style="Card.TLabel"
        ).pack(pady=20, padx=20, anchor="w")