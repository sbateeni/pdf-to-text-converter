import os
import tempfile
from docx import Document
from PyPDF2 import PdfFileReader
import fitz  # PyMuPDF


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_text_to_word(text_list, output_path):
    """Save a list of texts to a Word document."""
    try:
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        doc = Document()
        for text in text_list:
            doc.add_paragraph(text)
        doc.save(output_path)
        print(f"✅ Word document saved successfully at: {output_path}")
    except Exception as e:
        print(f"❌ Error in save_text_to_word: {str(e)}")
        raise


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def convert_pdf_to_word(pdf_path, output_dir):
    """Convert a PDF file to a Word document and save it in the specified output directory."""
    try:
        text = extract_text_from_pdf(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.docx")

        save_text_to_word([text], output_path)
        
        if os.path.exists(output_path):
            return output_path
        else:
            raise FileNotFoundError("Word file was not created after save_text_to_word operation")

    except Exception as e:
        print(f"❌ An error occurred during PDF to Word conversion: {str(e)}")
        return None
