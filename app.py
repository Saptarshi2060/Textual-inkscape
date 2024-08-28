import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import pdfplumber  # Install with: pip install pdfplumber
from tkinter import filedialog, Tk

# Define the font path (absolute path to the .ttf file)
font_path = r"C:\Users\User\Downloads\text_to_handwriting\QEDavidReidCAP.ttf"
font_size = 48  # You can adjust the size based on your preference

# Check if the font file exists
if not os.path.exists(font_path):
    print(f"Font file not found at {font_path}. Please check the path.")
    exit()

try:
    # Load the font
    font = ImageFont.truetype(font_path, font_size)
except OSError as e:
    print(f"Failed to load font. Error: {e}")
    exit()

# Function to convert text to handwritten image
def text_to_handwriting(text, output_image_name):
    # Calculate line height using getbbox
    line_height = font.getbbox("A")[3] - font.getbbox("A")[1]

    # Wrap text to fit within a certain width (in characters)
    lines = textwrap.wrap(text, width=40)  # Adjust width for wrapping

    # Calculate the required image height based on the number of lines
    image_height = line_height * len(lines) + 40  # Adding padding

    # Create an image with white background (adjust width to your preference)
    image_width = 800
    image = Image.new('RGB', (image_width, image_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw each line of text on the image
    y_position = 20  # Start position (padding from top)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (image_width - text_width) / 2
        draw.text((x_position, y_position), line, fill=(0, 0, 0), font=font)
        y_position += line_height

    # Save the image to a file
    image.save(output_image_name)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file_path):
    text = ""
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Main workflow
def main():
    # Initialize Tkinter root
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Prompt user to select a PDF file
    pdf_file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not pdf_file_path:
        print("No file selected. Exiting.")
        return

    # Extract text from the selected PDF
    text = extract_text_from_pdf(pdf_file_path)

    # Convert the extracted text to handwritten image(s)
    text_to_handwriting(text, "handwritten_output.png")

    print("Handwritten image saved as 'handwritten_output.png'.")

if __name__ == "__main__":
    main()
