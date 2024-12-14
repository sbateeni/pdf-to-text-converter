import streamlit as st
import os
import logging
from file_handling.file_processor import process_file
from text_processing.text_processor import process_text
import tempfile
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up page config
st.set_page_config(
    page_title="PDF to Text Converter",
    page_icon="📄",
    layout="wide"
)

def check_dependencies():
    """Check if required system dependencies are available."""
    try:
        # Check Tesseract
        pytesseract.get_tesseract_version()
        logger.info("Tesseract is available")
    except Exception as e:
        st.error("Tesseract is not properly installed. Some OCR features may not work.")
        logger.error(f"Tesseract error: {str(e)}")
        return False
    
    try:
        # Check Poppler by attempting to use pdf2image
        with tempfile.TemporaryDirectory() as temp_dir:
            test_pdf = os.path.join(temp_dir, "test.pdf")
            Path(test_pdf).touch()
            try:
                convert_from_path(test_pdf)
                logger.info("Poppler is available")
            except Exception as e:
                if "PDF file is corrupted" in str(e):
                    # This is actually good - it means poppler is installed and working
                    logger.info("Poppler is available")
                else:
                    raise
    except Exception as e:
        st.error("Poppler is not properly installed. Some PDF processing features may not work.")
        logger.error(f"Poppler error: {str(e)}")
        return False
    
    return True

def main():
    st.title("PDF to Text Converter")
    st.write("Upload your PDF file and convert it to text")

    # Check dependencies
    dependencies_ok = check_dependencies()
    if not dependencies_ok:
        st.warning("Some features may be limited due to missing dependencies.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner('Processing PDF...'):
            try:
                # Create a temporary directory for processing
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Save uploaded file
                    temp_pdf = os.path.join(temp_dir, uploaded_file.name)
                    with open(temp_pdf, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Process the file
                    text = process_file(uploaded_file)
                    
                    # Show processing options
                    st.subheader("Text Processing Options")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        remove_spaces = st.checkbox("Remove Extra Spaces")
                    with col2:
                        remove_special = st.checkbox("Remove Special Characters")
                    with col3:
                        make_lowercase = st.checkbox("Convert to Lowercase")
                    
                    # Process text with selected options
                    processed_text = process_text(text, {
                        'remove_extra_spaces': remove_spaces,
                        'remove_special_chars': remove_special,
                        'lowercase': make_lowercase
                    })
                    
                    # Display results
                    st.subheader("Extracted Text")
                    st.text_area("", processed_text, height=300)
                    
                    # Download button
                    st.download_button(
                        label="Download Text",
                        data=processed_text,
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}.txt",
                        mime="text/plain"
                    )
            
            except Exception as e:
                st.error(f"An error occurred while processing the PDF: {str(e)}")
                logger.error(f"Processing error: {str(e)}")

if __name__ == "__main__":
    main()