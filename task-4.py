import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np

class ImageToSketchConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Sketch Converter")

        self.original_image = None
        self.processed_image = None

        # Sketch parameters
        self.line_thickness = tk.DoubleVar()
        self.contrast = tk.DoubleVar()
        self.brightness = tk.DoubleVar()

        self.create_widgets()

    def create_widgets(self):
        # Create button to upload image
        self.upload_button = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        # Create label to display original image
        self.original_label = tk.Label(self.root)
        self.original_label.pack()

        # Create sliders for adjusting parameters
        self.line_thickness_label = tk.Label(self.root, text="Line Thickness")
        self.line_thickness_label.pack()
        self.line_thickness_slider = tk.Scale(self.root, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.line_thickness)
        self.line_thickness_slider.pack()

        self.contrast_label = tk.Label(self.root, text="Contrast")
        self.contrast_label.pack()
        self.contrast_slider = tk.Scale(self.root, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.contrast)
        self.contrast_slider.pack()

        self.brightness_label = tk.Label(self.root, text="Brightness")
        self.brightness_label.pack()
        self.brightness_slider = tk.Scale(self.root, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.brightness)
        self.brightness_slider.pack()

        # Create button to convert image to sketch
        self.convert_button = tk.Button(self.root, text="Convert to Sketch", command=self.convert_to_sketch, state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        # Create button to preview converted sketch
        self.preview_button = tk.Button(self.root, text="Preview", command=self.preview_sketch, state=tk.DISABLED)
        self.preview_button.pack(pady=5)

        # Create button to save converted sketch
        self.save_button = tk.Button(self.root, text="Save Sketch", command=self.save_sketch, state=tk.DISABLED)
        self.save_button.pack(pady=5)

        # Create label to display processed image (preview)
        self.processed_label = tk.Label(self.root)
        self.processed_label.pack()

    def upload_image(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
            if file_path:
                self.original_image = Image.open(file_path)
                self.display_image(self.original_image, self.original_label)
                self.convert_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")

    def convert_to_sketch(self):
        if self.original_image:
            try:
                # Adjust contrast and brightness
                enhanced_image = ImageEnhance.Contrast(self.original_image).enhance(self.contrast.get())
                enhanced_image = ImageEnhance.Brightness(enhanced_image).enhance(self.brightness.get())

                # Convert image to sketch
                gray_image = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2GRAY)
                inverted_blurred_image = cv2.bitwise_not(cv2.GaussianBlur(gray_image, (21, 21), 0))
                self.processed_image = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)
                self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_GRAY2RGB)
                self.processed_image = Image.fromarray(self.processed_image)
                self.display_image(self.processed_image, self.processed_label)
                self.preview_button.config(state=tk.NORMAL)
                self.save_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert image to sketch: {e}")

    def preview_sketch(self):
        if self.processed_image:
            try:
                preview_window = tk.Toplevel(self.root)
                preview_window.title("Sketch Preview")
                preview_label = tk.Label(preview_window)
                preview_label.pack()
                self.display_image(self.processed_image, preview_label)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to preview sketch: {e}")

    def save_sketch(self):
        if self.processed_image:
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp")])
                if file_path:
                    self.processed_image.save(file_path)
                    messagebox.showinfo("Save Sketch", "Sketch saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save sketch: {e}")

    def display_image(self, image, label):
        image.thumbnail((300, 300))
        imgtk = ImageTk.PhotoImage(image)
        label.config(image=imgtk)
        label.image = imgtk

# Create the main window
root = tk.Tk()

# Create an instance of ImageToSketchConverter
app = ImageToSketchConverter(root)

# Run the Tkinter event loop
root.mainloop()
