import streamlit as st
import tempfile
import os
from pathlib import Path
import logging
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from textblob import TextBlob
import arabic_reshaper
from bidi.algorithm import get_display

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="PDF to Text Converter",
    page_icon="📄",
    layout="wide"
)

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        # Check Tesseract
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
        return True
    except Exception as e:
        logger.error(f"Error checking dependencies: {str(e)}")
        return False

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyPDF2"""
    try:
        text = ""
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def perform_ocr(pdf_path, lang='eng'):
    """Perform OCR on PDF pages"""
    try:
        text = ""
        images = convert_from_path(pdf_path)
        for image in images:
            text += pytesseract.image_to_string(image, lang=lang) + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error performing OCR: {str(e)}")
        raise

def correct_text(text, lang):
    """Apply text corrections based on language"""
    try:
        if lang == 'ara':
            # Handle Arabic text
            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
        elif lang in ['eng', 'spa']:
            # Spell check for English and Spanish
            blob = TextBlob(text)
            return str(blob.correct())
        return text
    except Exception as e:
        logger.error(f"Error correcting text: {str(e)}")
        return text

def main():
    st.title("PDF to Text Converter")
    st.write("Upload your PDF file and convert it to text with support for English, Arabic, and Spanish")

    # Check dependencies
    if not check_dependencies():
        st.error("Some required dependencies are not available. Please check the logs for details.")
        return

    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Language selection
        lang = st.selectbox(
            "Select document language",
            options=['eng', 'ara', 'spa'],
            format_func=lambda x: {'eng': 'English', 'ara': 'Arabic', 'spa': 'Spanish'}[x]
        )

        # Processing options
        col1, col2, col3 = st.columns(3)
        with col1:
            use_ocr = st.checkbox("Use OCR", value=True)
        with col2:
            correct_spelling = st.checkbox("Correct spelling", value=True)
        with col3:
            remove_extra_spaces = st.checkbox("Remove extra spaces", value=True)

        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.TemporaryDirectory() as temp_dir:
                        pdf_path = Path(temp_dir) / "temp.pdf"
                        pdf_path.write_bytes(uploaded_file.getvalue())

                        # Extract text
                        if use_ocr:
                            text = perform_ocr(str(pdf_path), lang)
                        else:
                            text = extract_text_from_pdf(str(pdf_path))

                        # Post-process text
                        if correct_spelling:
                            text = correct_text(text, lang)
                        if remove_extra_spaces:
                            text = " ".join(text.split())

                        # Display results
                        st.subheader("Extracted Text")
                        st.text_area("", text, height=300)

                        # Download button
                        st.download_button(
                            label="Download Text",
                            data=text,
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.txt",
                            mime="text/plain"
                        )

                except Exception as e:
                    st.error(f"Error processing PDF: {str(e)}")
                    logger.error(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    main()