import cv2
import numpy as np

def embed_watermark(cover_img, watermark_img, delta=3):
    watermark_gray = cv2.cvtColor(watermark_img, cv2.COLOR_RGB2GRAY)
    _, watermark_binary = cv2.threshold(watermark_gray, 127, 1, cv2.THRESH_BINARY)
    
    h, w = cover_img.shape[:2]
    watermark_binary = cv2.resize(watermark_binary, (w, h))
    
    watermarked_img = cover_img.copy()
    
    watermarked_img[0, 0, 0] = w // 255
    watermarked_img[0, 1, 0] = w % 255
    watermarked_img[0, 2, 0] = h // 255
    watermarked_img[0, 3, 0] = h % 255
    
    for c in range(3):
        for i in range(h):
            for j in range(w):
                pixel_val = int(cover_img[i, j, c])
                wm_bit = watermark_binary[i, j]
                
                if wm_bit == 0:
                    quantized = delta * round(pixel_val / delta)
                else:
                    quantized = delta * round((pixel_val / delta) - 0.5) + delta // 2
                
                watermarked_img[i, j, c] = np.clip(quantized, 0, 255)
    
    return watermarked_img

def extract_watermark(watermarked_img, delta=3):
    h, w = watermarked_img.shape[:2]
    
    wm_w = int(watermarked_img[0, 0, 0]) * 255 + int(watermarked_img[0, 1, 0])
    wm_h = int(watermarked_img[0, 2, 0]) * 255 + int(watermarked_img[0, 3, 0])
    
    if wm_w <= 0 or wm_h <= 0 or wm_w > w or wm_h > h:
        wm_w, wm_h = w, h
    
    extracted = np.zeros((h, w), dtype=np.uint8)
    
    for c in range(3):
        for i in range(h):
            for j in range(w):
                pixel_val = int(watermarked_img[i, j, c])
                remainder = pixel_val % delta
                
                if remainder < delta // 2:
                    extracted[i, j] += 0
                else:
                    extracted[i, j] += 1
    
    extracted = (extracted >= 2).astype(np.uint8) * 255
    
    extracted = cv2.medianBlur(extracted, 3)
    
    return cv2.cvtColor(extracted, cv2.COLOR_GRAY2RGB)