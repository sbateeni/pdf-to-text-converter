import PyPDF2
import logging
from pathlib import Path
import tempfile
import os
from io import BytesIO

logger = logging.getLogger(__name__)

def process_file(uploaded_file):
    """
    Process the uploaded PDF file and extract text from it.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit
    
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Read PDF directly from BytesIO
        pdf_bytes = BytesIO(uploaded_file.getvalue())
        
        # Extract text from PDF
        text = ""
        pdf_reader = PyPDF2.PdfReader(pdf_bytes)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise Exception(f"Failed to process PDF file: {str(e)}")
