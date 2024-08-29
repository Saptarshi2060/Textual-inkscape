import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import PyPDF2

# Define the font path and size
font_path = "path to your font"
font_size = 24  # Adjust the size as needed

# Load the font
font = ImageFont.truetype(font_path, font_size)

# Define the output image size
image_width = 2480  # A4 width in pixels at 300 dpi
image_height = 3508  # A4 height in pixels at 300 dpi

# Load the PDF
pdf_path = "path to pdf"
with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

# Process paragraphs by replacing line breaks within paragraphs with spaces
paragraphs = text.replace("\n", " ").split("  ")  # Two spaces for paragraph separation

# Create an output image
image = Image.new("RGB", (image_width, image_height), "white")
draw = ImageDraw.Draw(image)

# Define text margins
margin_left = 200
margin_top = 100
current_y = margin_top

# Calculate line height based on the font size
_, _, _, line_height = draw.textbbox((0, 0), "A", font=font)
line_height += 5  # Add a small buffer to ensure proper spacing

# Process each paragraph
for para in paragraphs:
    # Split the paragraph into words to handle wrapping manually
    words = para.split()
    current_line = ""

    for word in words:
        # Check if adding the next word would exceed the width
        test_line = f"{current_line} {word}".strip()
        _, _, test_width, _ = draw.textbbox((0, 0), test_line, font=font)

        if test_width <= image_width - 2 * margin_left:
            # Add the word to the current line
            current_line = test_line
        else:
            # Draw the current line and start a new one
            draw.text((margin_left, current_y), current_line, font=font, fill="black")
            current_y += line_height
            current_line = word  # Start new line with the current word

    # Draw the last line of the paragraph
    if current_line:
        draw.text((margin_left, current_y), current_line, font=font, fill="black")
        current_y += line_height

    # Add space between paragraphs
    current_y += line_height * 0.5  # Adjust spacing between paragraphs

# Save the image
output_path = "handwritten_output.png"
image.save(output_path)

print(f"Handwritten image saved to {output_path}")
