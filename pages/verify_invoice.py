import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
from PIL import Image, ImageTk
from utils.watermark import extract_watermark

class VerifyInvoicePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.watermarked_img = None
        self.extracted_watermark = None
        
        self.create_widgets()
    
    def create_widgets(self):
        header = ttk.Frame(self, style="Primary.TFrame")
        header.pack(fill="x", pady=10)
        
        ttk.Label(
            header,
            text="Verify Invoice Authenticity",
            font=("Helvetica", 18, "bold"),
            style="Primary.TLabel"
        ).pack(pady=10)
        
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        left_panel = ttk.LabelFrame(main_frame, text="Watermarked Invoice", padding=10)
        left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Button(
            left_panel,
            text="Load Watermarked Invoice",
            command=self.load_watermarked_image,
            style="Accent.TButton"
        ).pack(pady=10)
        
        self.watermarked_canvas = tk.Canvas(left_panel, width=400, height=500, bg="#f0f0f0")
        self.watermarked_canvas.pack(pady=10)
        
        right_panel = ttk.LabelFrame(main_frame, text="Extracted Watermark", padding=10)
        right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ttk.Button(
            right_panel,
            text="Extract Watermark",
            command=self.extract_watermark,
            style="Accent.TButton"
        ).pack(pady=10)
        
        ttk.Button(
            right_panel,
            text="Save Watermark",
            command=self.save_watermark
        ).pack(pady=5)
        
        self.extracted_canvas = tk.Canvas(right_panel, width=400, height=500, bg="#f0f0f0")
        self.extracted_canvas.pack(pady=10)
        
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
    
    def load_watermarked_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.watermarked_img = cv2.imread(file_path)
            self.watermarked_img = cv2.cvtColor(self.watermarked_img, cv2.COLOR_BGR2RGB)
            self.display_image(self.watermarked_img, self.watermarked_canvas, (400, 500))
    
    def extract_watermark(self):
        if self.watermarked_img is None:
            messagebox.showerror("Error", "Please load a watermarked image first")
            return
            
        self.extracted_watermark = extract_watermark(self.watermarked_img)
        self.display_image(self.extracted_watermark, self.extracted_canvas, (400, 500))
        messagebox.showinfo("Success", "Watermark extracted successfully")
    
    def save_watermark(self):
        if self.watermarked_img is None:
            messagebox.showerror("Error", "No watermarked image to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.watermarked_img, cv2.COLOR_RGB2BGR))
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
    