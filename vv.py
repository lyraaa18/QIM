import datetime
import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageFont, ImageDraw
import numpy as np
import cv2
from matplotlib import pyplot as plt
import io

class WatermarkApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Watermarking App")
        self.root.geometry("1000x700")
        
        self.cover_image = None
        self.watermark_image = None
        self.watermarked_image = None
        self.extracted_watermark = None
        self.original_watermarked_size = (0,0)
        
        self.delta = 3
        self.strenght = 0
        self.create_widgets()
    
    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.embed_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.embed_frame, text="Embed Watermark")
        
        self.extract_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.extract_frame, text="Extract Watermark")
        
        self.setup_embed_frame()
        self.setup_extract_frame()

    def generate_invoice(self):
        try:
            invoice_number = simpledialog.askstring("Invoice Details", "Invoice Number:", initialvalue=f"INV-{random.randint(10000, 99999)}")
            if not invoice_number:
                return
                
            customer_name = simpledialog.askstring("Invoice Details", "Customer Name:", initialvalue="John Doe")
            if not customer_name:
                return
                
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
            
            draw.text((50, 50), "INVOICE", fill="black", font=font_large)
            draw.text((50, 90), f"Invoice #: {invoice_number}", fill="black", font=font_medium)
            draw.text((50, 120), f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", fill="black", font=font_medium)
            
            draw.text((width-250, 50), "Your Company Name", fill="black", font=font_medium)
            draw.text((width-250, 80), "123 Business St", fill="black", font=font_small)
            draw.text((width-250, 100), "City, State ZIP", fill="black", font=font_small)
            draw.text((width-250, 120), "Phone: (123) 456-7890", fill="black", font=font_small)
            
            draw.text((50, 180), "Bill To:", fill="black", font=font_medium)
            draw.text((50, 210), customer_name, fill="black", font=font_small)
            draw.text((50, 230), "Customer Address Line 1", fill="black", font=font_small)
            draw.text((50, 250), "Customer City, State ZIP", fill="black", font=font_small)
            
            draw.rectangle([(50, 300), (width-50, 330)], outline="black", fill="#EEEEEE")
            draw.text((60, 305), "Item", fill="black", font=font_medium)
            draw.text((350, 305), "Quantity", fill="black", font=font_medium)
            draw.text((450, 305), "Unit Price", fill="black", font=font_medium)
            draw.text((600, 305), "Amount", fill="black", font=font_medium)
            
            items = [
                ("Product 1", 2, 50.00),
                ("Service A", 1, 100.00),
                ("Maintenance", 3, 25.00)
            ]
            
            y_pos = 340
            total = 0
            
            for item in items:
                name, qty, price = item
                amount = qty * price
                total += amount
                
                draw.line([(50, y_pos), (width-50, y_pos)], fill="black")
                draw.text((60, y_pos+10), name, fill="black", font=font_small)
                draw.text((350, y_pos+10), str(qty), fill="black", font=font_small)
                draw.text((450, y_pos+10), f"${price:.2f}", fill="black", font=font_small)
                draw.text((600, y_pos+10), f"${amount:.2f}", fill="black", font=font_small)
                
                y_pos += 40
            
            draw.line([(50, y_pos), (width-50, y_pos)], fill="black")
            draw.line([(50, y_pos+40), (width-50, y_pos+40)], fill="black")
            draw.text((500, y_pos+10), "Total:", fill="black", font=font_medium)
            draw.text((600, y_pos+10), f"${total:.2f}", fill="black", font=font_medium)
            
            draw.text((width//2-100, y_pos+60), "Thank you for your business!", fill="black", font=font_medium)
            
            self.cover_image = np.array(img)
            self.cover_image = cv2.cvtColor(self.cover_image, cv2.COLOR_RGB2BGR)
            self.cover_image = cv2.cvtColor(self.cover_image, cv2.COLOR_BGR2RGB)
            
            self.display_image(self.cover_image, self.cover_canvas, (400, 400))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice: {str(e)}")

    def setup_embed_frame(self):
        left_frame = ttk.LabelFrame(self.embed_frame, text="Cover Image (Invoice)")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.cover_canvas = tk.Canvas(left_frame, width=400, height=400, bg="light gray")
        self.cover_canvas.pack(padx=10, pady=10)
        
        cover_button_frame = ttk.Frame(left_frame)
        cover_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(cover_button_frame, text="Load Invoice", command=self.load_cover_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(cover_button_frame, text="Generate Invoice", command=self.generate_invoice).pack(side=tk.LEFT, padx=5)
        
        middle_frame = ttk.LabelFrame(self.embed_frame, text="Watermark Image")
        middle_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.watermark_canvas = tk.Canvas(middle_frame, width=200, height=200, bg="light gray")
        self.watermark_canvas.pack(padx=10, pady=10)
        
        watermark_button_frame = ttk.Frame(middle_frame)
        watermark_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(watermark_button_frame, text="Load Watermark", command=self.load_watermark_image).pack(side=tk.LEFT, padx=5)
        
        right_frame = ttk.LabelFrame(self.embed_frame, text="Watermarked Result")
        right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        self.result_canvas = tk.Canvas(right_frame, width=400, height=400, bg="light gray")
        self.result_canvas.pack(padx=10, pady=10)
        
        result_button_frame = ttk.Frame(right_frame)
        result_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(result_button_frame, text="Embed Watermark", command=self.embed_watermark).pack(side=tk.LEFT, padx=5)
        ttk.Button(result_button_frame, text="Save Result", command=self.save_watermarked_image).pack(side=tk.LEFT, padx=5)
        
        self.embed_frame.grid_columnconfigure(0, weight=1)
        self.embed_frame.grid_columnconfigure(1, weight=1)
        self.embed_frame.grid_columnconfigure(2, weight=1)
        self.embed_frame.grid_rowconfigure(0, weight=1)
    
    def setup_extract_frame(self):
        left_frame = ttk.LabelFrame(self.extract_frame, text="Watermarked Image")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.watermarked_canvas = tk.Canvas(left_frame, width=400, height=400, bg="light gray")
        self.watermarked_canvas.pack(padx=10, pady=10)
        
        watermarked_button_frame = ttk.Frame(left_frame)
        watermarked_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(watermarked_button_frame, text="Load Watermarked Image", 
                 command=self.load_watermarked_image).pack(side=tk.LEFT, padx=5)
                 
        right_frame = ttk.LabelFrame(self.extract_frame, text="Extracted Watermark")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.extracted_canvas = tk.Canvas(right_frame, width=400, height=400, bg="light gray")
        self.extracted_canvas.pack(padx=10, pady=10)
        
        extracted_button_frame = ttk.Frame(right_frame)
        extracted_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(extracted_button_frame, text="Extract Watermark", 
                 command=self.extract_watermark).pack(side=tk.LEFT, padx=5)
        ttk.Button(extracted_button_frame, text="Save Extracted Watermark", 
                 command=self.save_extracted_watermark).pack(side=tk.LEFT, padx=5)
        
        self.extract_frame.grid_columnconfigure(0, weight=1)
        self.extract_frame.grid_columnconfigure(1, weight=1)
        self.extract_frame.grid_rowconfigure(0, weight=1)

    def load_cover_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            try:
                self.cover_image = cv2.imread(file_path)
                self.cover_image = cv2.cvtColor(self.cover_image, cv2.COLOR_BGR2RGB)
                self.display_image(self.cover_image, self.cover_canvas, (400, 400))
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load cover image: {str(e)}")
    
    def load_watermark_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Watermark Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            try:
                self.watermark_image = cv2.imread(file_path)
                self.watermark_image = cv2.cvtColor(self.watermark_image, cv2.COLOR_BGR2RGB)
                
                self.display_image(self.watermark_image, self.watermark_canvas, (200, 200))
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load watermark image: {str(e)}")
    
    def load_watermarked_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Watermarked Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            try:
                self.watermarked_image = cv2.imread(file_path)
                self.watermarked_image = cv2.cvtColor(self.watermarked_image, cv2.COLOR_BGR2RGB)
                self.display_image(self.watermarked_image, self.watermarked_canvas, (400, 400))
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load watermarked image: {str(e)}")
    
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
    
    def embed_watermark(self):
        if self.cover_image is None or self.watermark_image is None:
            messagebox.showerror("Error", "Both cover image and watermark must be loaded first")
            return
            
        try:
            watermark_gray = cv2.cvtColor(self.watermark_image, cv2.COLOR_RGB2GRAY)
            _, watermark_binary = cv2.threshold(watermark_gray, 127, 1, cv2.THRESH_BINARY)
            
            cover_img = self.cover_image.copy()
            cover_h, cover_w = cover_img.shape[:2]
            wm_h, wm_w = watermark_binary.shape[:2]
            
            if wm_h != cover_h or wm_w != cover_w:
                watermark_binary = cv2.resize(watermark_binary, (cover_w, cover_h))
                wm_h, wm_w = watermark_binary.shape[:2]
                
            self.watermarked_image = cover_img.copy()
            self.watermarked_image[0, 0, 0] = wm_w // 255
            self.watermarked_image[0, 1, 0] = wm_w % 255
            self.watermarked_image[0, 2, 0] = wm_h // 255
            self.watermarked_image[0, 3, 0] = wm_h % 255
            

            for c in range(3):  # Process all color channels
                for i in range(wm_h):
                    for j in range(wm_w):
                        if i < cover_h and j < cover_w:
                            pixel_val = int(cover_img[i, j, c])
                            wm_bit = watermark_binary[i, j]
                            
                            # Apply QIM
                            if wm_bit == 0:
                                quantized = self.delta * round(pixel_val / self.delta)
                            else:
                                quantized = self.delta * round((pixel_val / self.delta) - 0.5) + self.delta // 2
                            
                            # Ensure value is within range
                            quantized = max(0, min(255, quantized))
                            self.watermarked_image[i, j, c] = quantized
            
            # Display result
            self.display_image(self.watermarked_image, self.result_canvas, (400, 400))
            messagebox.showinfo("Success", "Watermark embedded successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to embed watermark: {str(e)}")
    
    def extract_watermark(self):
        if self.watermarked_image is None:
            messagebox.showerror("Error", "A watermarked image must be loaded first")
            return
            
        try:
            wm_img = self.watermarked_image.copy()
            h, w = wm_img.shape[:2]
            
            # Get the watermark dimensions from the first pixels
            wm_w = int(wm_img[0, 0, 0]) * 255 + int(wm_img[0, 1, 0])
            wm_h = int(wm_img[0, 2, 0]) * 255 + int(wm_img[0, 3, 0])
            
            # If dimensions are incorrect, use the image dimensions
            if wm_w <= 0 or wm_h <= 0 or wm_w > w or wm_h > h:
                wm_w, wm_h = w, h
                
            self.extracted_watermark = np.zeros((h, w), dtype=np.uint8)
            
            # Extract watermark from all color channels and combine
            watermark_channels = []
            for c in range(3):
                channel_watermark = np.zeros((h, w), dtype=np.uint8)
                for i in range(h):
                    for j in range(w):
                        pixel_val = int(wm_img[i, j, c])
                        
                        # Apply QIM extraction
                        remainder = pixel_val % self.delta
                        if remainder < self.delta // 2:
                            channel_watermark[i, j] = 0
                        else:
                            channel_watermark[i, j] = 1
                watermark_channels.append(channel_watermark)
            
            # Combine the watermarks from different channels
            for i in range(h):
                for j in range(w):
                    # Use majority voting to determine the watermark bit
                    bit_sum = int(watermark_channels[0][i, j]) + int(watermark_channels[1][i, j]) + int(watermark_channels[2][i, j])
                    if bit_sum >= 2:  # Majority vote
                        self.extracted_watermark[i, j] = 1
                    else:
                        self.extracted_watermark[i, j] = 0
            
            # Scale to 0-255 for display
            self.extracted_watermark = self.extracted_watermark * 255
            
            # Apply some post-processing to clean up the extracted watermark
            self.extracted_watermark = cv2.medianBlur(self.extracted_watermark, 3)
            
            # Convert to RGB for display
            extracted_rgb = cv2.cvtColor(self.extracted_watermark, cv2.COLOR_GRAY2RGB)
            self.display_image(extracted_rgb, self.extracted_canvas, (400, 400))
            messagebox.showinfo("Success", "Watermark extracted successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract watermark: {str(e)}")
 
    def save_watermarked_image(self):
        if self.watermarked_image is None:
            messagebox.showerror("Error", "No watermarked image to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Watermarked Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                save_img = cv2.cvtColor(self.watermarked_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, save_img)
                messagebox.showinfo("Success", f"Watermarked image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def save_extracted_watermark(self):
        if self.extracted_watermark is None:
            messagebox.showerror("Error", "No extracted watermark to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Extracted Watermark",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                cv2.imwrite(file_path, self.extracted_watermark)
                messagebox.showinfo("Success", f"Extracted watermark saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()