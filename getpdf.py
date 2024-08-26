from pdf2image import convert_from_path

# Path to the PDF file
pdf_path = 'SFU_SR_C62_L (4).pdf'

# Convert PDF to images
images = convert_from_path(pdf_path)

# Save each page as an image
for i, image in enumerate(images):
    image.save(f'output_page_{i + 1}.jpeg', 'JPEG')  # Change 'PNG' to 'JPEG' for JPEG format