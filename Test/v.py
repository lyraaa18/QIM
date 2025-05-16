import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
from matplotlib import pyplot as plt
import io

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QIM Watermarking App")
        self.root.geometry("1000x700")

        self.cover_image = None
        self.watermark_image = None
        self.watermarked_image = None
        self.extracted_watermark = None
        
        self.delta = 30 
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create embedding tab
        self.embed_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.embed_frame, text="Embed Watermark")
        
        # Create extraction tab
        self.extract_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.extract_frame, text="Extract Watermark")
        
        # Set up embedding tab
        self.setup_embed_frame()
        
        # Set up extraction tab
        self.setup_extract_frame()
        
        # Parameter control frame
        self.param_frame = ttk.LabelFrame(self.root, text="QIM Parameters")
        self.param_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Delta parameter
        ttk.Label(self.param_frame, text="Delta (Strength):").grid(row=0, column=0, padx=5, pady=5)
        self.delta_scale = ttk.Scale(self.param_frame, from_=5, to=50, orient=tk.HORIZONTAL,
        length=200, value=self.delta, command=self.update_delta)
        self.delta_scale.grid(row=0, column=1, padx=5, pady=5)
        self.delta_label = ttk.Label(self.param_frame, text=f"{self.delta}")
        self.delta_label.grid(row=0, column=2, padx=5, pady=5)
    
    def setup_embed_frame(self):
        # Left side - Cover Image
        left_frame = ttk.LabelFrame(self.embed_frame, text="Cover Image (Invoice)")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.cover_canvas = tk.Canvas(left_frame, width=400, height=400, bg="light gray")
        self.cover_canvas.pack(padx=10, pady=10)
        
        cover_button_frame = ttk.Frame(left_frame)
        cover_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(cover_button_frame, text="Load Invoice", command=self.load_cover_image).pack(side=tk.LEFT, padx=5)
        
        # Middle - Watermark Image
        middle_frame = ttk.LabelFrame(self.embed_frame, text="Watermark Image")
        middle_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.watermark_canvas = tk.Canvas(middle_frame, width=200, height=200, bg="light gray")
        self.watermark_canvas.pack(padx=10, pady=10)
        
        watermark_button_frame = ttk.Frame(middle_frame)
        watermark_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(watermark_button_frame, text="Load Watermark", command=self.load_watermark_image).pack(side=tk.LEFT, padx=5)
        
        # Right side - Watermarking controls and result
        right_frame = ttk.LabelFrame(self.embed_frame, text="Watermarked Result")
        right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        self.result_canvas = tk.Canvas(right_frame, width=400, height=400, bg="light gray")
        self.result_canvas.pack(padx=10, pady=10)
        
        result_button_frame = ttk.Frame(right_frame)
        result_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(result_button_frame, text="Embed Watermark", command=self.embed_watermark).pack(side=tk.LEFT, padx=5)
        ttk.Button(result_button_frame, text="Save Result", command=self.save_watermarked_image).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        self.embed_frame.grid_columnconfigure(0, weight=1)
        self.embed_frame.grid_columnconfigure(1, weight=1)
        self.embed_frame.grid_columnconfigure(2, weight=1)
        self.embed_frame.grid_rowconfigure(0, weight=1)
    
    def setup_extract_frame(self):
        # Left side - Watermarked Image
        left_frame = ttk.LabelFrame(self.extract_frame, text="Watermarked Image")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.watermarked_canvas = tk.Canvas(left_frame, width=400, height=400, bg="light gray")
        self.watermarked_canvas.pack(padx=10, pady=10)
        
        watermarked_button_frame = ttk.Frame(left_frame)
        watermarked_button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(watermarked_button_frame, text="Load Watermarked Image", 
                 command=self.load_watermarked_image).pack(side=tk.LEFT, padx=5)
                 
        # Right side - Extracted Watermark
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
        
        # Configure grid weights
        self.extract_frame.grid_columnconfigure(0, weight=1)
        self.extract_frame.grid_columnconfigure(1, weight=1)
        self.extract_frame.grid_rowconfigure(0, weight=1)
    
    def update_delta(self, val):
        self.delta = int(float(val))
        self.delta_label.config(text=f"{self.delta}")
    
    def load_cover_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            try:
                # Open and display the cover image
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
                # Open and display the watermark image
                self.watermark_image = cv2.imread(file_path)
                self.watermark_image = cv2.cvtColor(self.watermark_image, cv2.COLOR_BGR2RGB)
                
                # Resize watermark to match dimensions (or portion) of cover image
                if self.cover_image is not None:
                    h, w = self.cover_image.shape[:2]
                    # Resize watermark to be proportional to cover image size
                    wm_h, wm_w = min(h // 2, 200), min(w // 2, 200)
                    self.watermark_image = cv2.resize(self.watermark_image, (wm_w, wm_h))
                
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
                # Open and display the watermarked image
                self.watermarked_image = cv2.imread(file_path)
                self.watermarked_image = cv2.cvtColor(self.watermarked_image, cv2.COLOR_BGR2RGB)
                self.display_image(self.watermarked_image, self.watermarked_canvas, (400, 400))
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load watermarked image: {str(e)}")
    
    def display_image(self, img, canvas, size):
        if img is None:
            return
            
        # Resize the image for display
        h, w = img.shape[:2]
        aspect_ratio = w / h
        
        if aspect_ratio > 1:  # Wider than tall
            new_w = size[0]
            new_h = int(size[0] / aspect_ratio)
        else:  # Taller than wide
            new_h = size[1]
            new_w = int(size[1] * aspect_ratio)
        
        # Resize for display only
        display_img = cv2.resize(img.copy(), (new_w, new_h))
        
        # Convert to PhotoImage
        pil_img = Image.fromarray(display_img)
        photo_img = ImageTk.PhotoImage(image=pil_img)
        
        # Update canvas
        canvas.config(width=new_w, height=new_h)
        canvas.create_image(new_w // 2, new_h // 2, image=photo_img, anchor=tk.CENTER)
        canvas.image = photo_img  # Keep a reference to prevent garbage collection
    
    def embed_watermark(self):
        if self.cover_image is None or self.watermark_image is None:
            messagebox.showerror("Error", "Both cover image and watermark must be loaded first")
            return
            
        try:
            # Convert watermark to binary (0 and 1) for embedding
            watermark_gray = cv2.cvtColor(self.watermark_image, cv2.COLOR_RGB2GRAY)
            _, watermark_binary = cv2.threshold(watermark_gray, 127, 1, cv2.THRESH_BINARY)
            
            # Prepare cover image
            cover_img = self.cover_image.copy()
            
            # Get dimensions
            cover_h, cover_w = cover_img.shape[:2]
            wm_h, wm_w = watermark_binary.shape[:2]
            
            # Prepare watermarked image
            self.watermarked_image = cover_img.copy()
            
            # Embed watermark using QIM
            for c in range(3):  # For each color channel
                for i in range(wm_h):
                    for j in range(wm_w):
                        if i < cover_h and j < cover_w:  # Make sure we're within cover image bounds
                            pixel_val = int(cover_img[i, j, c])
                            wm_bit = watermark_binary[i, j]
                            
                            # QIM embedding - quantize to even or odd multiples based on watermark bit
                            if wm_bit == 0:
                                quantized = self.delta * round(pixel_val / self.delta)
                            else:
                                quantized = self.delta * round((pixel_val / self.delta) - 0.5) + self.delta // 2
                            
                            # Clip to valid pixel range
                            quantized = max(0, min(255, quantized))
                            self.watermarked_image[i, j, c] = quantized
            
            # Display the watermarked image
            self.display_image(self.watermarked_image, self.result_canvas, (400, 400))
            messagebox.showinfo("Success", "Watermark embedded successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to embed watermark: {str(e)}")
    
    def extract_watermark(self):
        if self.watermarked_image is None:
            messagebox.showerror("Error", "A watermarked image must be loaded first")
            return
            
        try:
            # Get dimensions
            wm_img = self.watermarked_image.copy()
            h, w = wm_img.shape[:2]
            
            # Initialize extracted watermark
            self.extracted_watermark = np.zeros((h, w), dtype=np.uint8)
            
            # Extract the watermark using QIM
            for c in range(3):  # Use blue channel for extraction
                for i in range(h):
                    for j in range(w):
                        pixel_val = int(wm_img[i, j, c])
                        
                        # QIM extraction - check if closer to even or odd multiples
                        remainder = pixel_val % self.delta
                        if remainder < self.delta // 2:
                            self.extracted_watermark[i, j] = 0
                        else:
                            self.extracted_watermark[i, j] = 1
            
            # Convert to display format
            self.extracted_watermark = self.extracted_watermark * 255
            
            # Apply median filter to reduce noise
            self.extracted_watermark = cv2.medianBlur(self.extracted_watermark, 3)
            
            # Display extracted watermark
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
                # Convert from RGB to BGR for OpenCV
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