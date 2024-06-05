# Made by Gokef (Have to install tesseract)

import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

# Set up Tesseract executable path (change this path based on your installation)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Text")
        
        self.label = tk.Label(root, text="Select an image file:")
        self.label.pack(pady=10)
        
        self.select_button = tk.Button(root, text="Browse", command=self.browse_image)
        self.select_button.pack(pady=10)

        self.lang_label = tk.Label(root, text="Select Image Language:")
        self.lang_label.pack(pady=5)

        self.language_var = tk.StringVar()
        self.language_combobox = ttk.Combobox(root, textvariable=self.language_var)
        self.language_combobox['values'] = ('eng', 'tur')  # Add more languages as needed
        self.language_combobox.current(0)
        self.language_combobox.pack(pady=5)
        
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)
        
        self.text_label = tk.Text(root, wrap=tk.WORD, width=60, height=15)
        self.text_label.pack(pady=10)
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.extract_text(file_path)
    
    def preprocess_image(self, img):
        # Convert image to grayscale
        img = img.convert("L")
        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        # Apply thresholding
        img = img.point(lambda x: 0 if x < 140 else 255)
        # Apply some additional sharpening
        img = img.filter(ImageFilter.SHARPEN)
        return img
    
    def extract_text(self, file_path):
        try:
            img = Image.open(file_path)
            processed_img = self.preprocess_image(img)
            img.thumbnail((400, 400))  # Resize for display purposes
            img_tk = ImageTk.PhotoImage(img)
            
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
            
            selected_language = self.language_var.get()
            text = pytesseract.image_to_string(processed_img, lang=selected_language)  # Use selected language
            self.text_label.delete(1.0, tk.END)
            self.text_label.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text from image. Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
