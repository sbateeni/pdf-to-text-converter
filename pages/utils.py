import os
import fitz  # PyMuPDF
from docx import Document
from fpdf import FPDF

def allowed_file(filename, allowed_extensions={'pdf'}):
    """Check if the uploaded file is an allowed type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def convert_pdf_to_images(pdf_path, output_dir):
    """Convert a PDF file into images, one per page."""
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    images = []
    for page_num in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_num)
        # Render the page to an image
        pix = page.get_pixmap()
        img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(img_path)
        images.append(img_path)
    return images

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def save_text_to_word(texts, output_path):
    """Save extracted text to a Word document."""
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a new Word document
    doc = Document()
    for i, text in enumerate(texts):
        doc.add_heading(f'Page {i + 1}', level=1)
        doc.add_paragraph(text)

    # Save the document to the specified path
    doc.save(output_path)

def save_text_to_pdf(text, output_path):
    """Save extracted text to a PDF file."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(output_path)

def count_words_in_text(text, search_word):
    """Count the occurrences of a word in the text."""
    return text.lower().count(search_word.lower())

def convert_pdf_to_word(pdf_path, output_dir):
    """Convert a PDF file to a Word document."""
    text = extract_text_from_pdf(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}.docx")
    save_text_to_word([text], output_path)  # Wrap text in a list
    return output_path
