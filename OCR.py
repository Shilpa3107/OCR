import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog, scrolledtext

# Select image file
tk.Tk().withdraw()
image_path = filedialog.askopenfilename(
    title='Select an Image',
    filetypes=[('Image Files', '*.png *.jpg *.jpeg *.bmp *.tiff')]
)

if not image_path:
    print("No image selected.")
    exit()

# Run OCR
reader = easyocr.Reader(['en'], gpu=False)
results = reader.readtext(image_path)

# Show image with bounding boxes
image = cv2.imread(image_path)
for (bbox, text, prob) in results:
    (tl, tr, br, bl) = bbox
    tl = tuple(map(int, tl))
    br = tuple(map(int, br))
    cv2.rectangle(image, tl, br, (0, 255, 0), 2)
    cv2.putText(image, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# Convert and show using matplotlib
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(10, 10))
plt.imshow(image_rgb)
plt.axis('off')
plt.title('OCR Result')
plt.show()

# GUI window to copy text
text_window = tk.Tk()
text_window.title("Copy Detected Text")

# ScrolledText for output
text_area = scrolledtext.ScrolledText(text_window, wrap=tk.WORD, width=80, height=20, font=("Courier", 12))
text_area.pack(padx=10, pady=10)

# Join all text
text_content = "\n".join([text for (_, text, _) in results])
text_area.insert(tk.END, text_content)
text_area.configure(state='normal')  # Keep it editable for copy

# Clipboard copy function
def copy_to_clipboard():
    text_window.clipboard_clear()
    text_window.clipboard_append(text_content)
    text_window.update()

# Add a copy button
copy_btn = tk.Button(text_window, text="Copy All to Clipboard", command=copy_to_clipboard)
copy_btn.pack(pady=5)

text_window.mainloop()
