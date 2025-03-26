import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def pdf_to_images(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    page_images = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        output_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(output_path)
        page_images.append(output_path)
    return page_images

def pdf_to_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text_pages = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        text_pages.append(text)
    return text_pages

def text_to_handwritten_image(text, font_path, output_path, image_width=800, line_height=40):
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")
    
    font = ImageFont.truetype(font_path, size=30)
    lines = text.split('\n')
    image_height = line_height * len(lines)
    image = Image.new(mode="RGB", size=(image_width, image_height), color="white")
    draw = ImageDraw.Draw(image)
    
    y_text = 0
    for line in lines:
        draw.text((10, y_text), line, font=font, fill="black")
        y_text += line_height
    
    image.save(output_path)

def convert_pdf_to_handwritten(pdf_path, font_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    text_pages = pdf_to_text(pdf_path)
    for i, text in enumerate(text_pages):
        output_path = os.path.join(output_folder, f"handwritten_page_{i + 1}.png")
        text_to_handwritten_image(text, font_path, output_path)

    messagebox.showinfo("Success", f"Handwritten images saved to {output_folder}")

def select_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        font_path = filedialog.askopenfilename(title="Select Handwriting Font", filetypes=[("Font files", "*.ttf")])
        if font_path:
            output_folder = filedialog.askdirectory(title="Select Output Folder")
            if output_folder:
                convert_pdf_to_handwritten(pdf_path, font_path, output_folder)

def create_app():
    root = tk.Tk()
    root.title("PDF to Handwritten Converter")
    root.geometry("400x200")

    select_button = tk.Button(root, text="Select PDF to Convert", command=select_pdf)
    select_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_app()
