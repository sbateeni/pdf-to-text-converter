import streamlit as st
import tempfile
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
import logging
from PIL import Image
import arabic_reshaper
from bidi.algorithm import get_display
from textblob import TextBlob

logger = logging.getLogger(__name__)

st.set_page_config(page_title="OCR Processing", page_icon="🔍", layout="wide")

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
            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
        elif lang in ['eng', 'spa']:
            blob = TextBlob(text)
            return str(blob.correct())
        return text
    except Exception as e:
        logger.error(f"Error correcting text: {str(e)}")
        return text

def main():
    st.title("OCR Processing")
    st.write("Extract text from scanned PDFs or images using OCR")

    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Language selection
        lang = st.selectbox(
            "Select document language",
            options=['eng', 'ara', 'spa'],
            format_func=lambda x: {'eng': 'English', 'ara': 'Arabic', 'spa': 'Spanish'}[x]
        )

        # Processing options
        col1, col2 = st.columns(2)
        with col1:
            correct_spelling = st.checkbox("Correct spelling", value=True)
        with col2:
            remove_extra_spaces = st.checkbox("Remove extra spaces", value=True)

        if st.button("Process Document"):
            with st.spinner("Processing..."):
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        file_path = Path(temp_dir) / uploaded_file.name
                        file_path.write_bytes(uploaded_file.getvalue())

                        if uploaded_file.type == "application/pdf":
                            text = perform_ocr(str(file_path), lang)
                        else:
                            # For image files
                            image = Image.open(file_path)
                            text = pytesseract.image_to_string(image, lang=lang)

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
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}_ocr.txt",
                            mime="text/plain"
                        )

                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")
                    logger.error(f"Error processing document: {str(e)}")

if __name__ == "__main__":
    main()
