import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
from tkinter import Tk, filedialog

# Suppress tkinter root window
Tk().withdraw()

# Let user choose an image file
image_path = filedialog.askopenfilename(
    title='Select an Image',
    filetypes=[('Image Files', '*.png *.jpg *.jpeg *.bmp *.tiff')]
)

if not image_path:
    print("No image selected.")
    exit()

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Perform OCR
results = reader.readtext(image_path)

# Display the image using OpenCV
image = cv2.imread(image_path)

# Draw OCR results on the image
for (bbox, text, prob) in results:
    # Unpack the bounding box
    (top_left, top_right, bottom_right, bottom_left) = bbox
    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))

    # Draw rectangle and text
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image, text, (top_left[0], top_left[1] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# Convert BGR to RGB for displaying with matplotlib
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Show the result
plt.figure(figsize=(10, 10))
plt.imshow(image_rgb)
plt.axis('off')
plt.title('OCR Result')
plt.show()

# Print detected text to console
print("\nDetected Text:")
for (_, text, _) in results:
    print(text)
