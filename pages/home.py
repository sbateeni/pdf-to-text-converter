import streamlit as st
import os
import time
from tempfile import TemporaryDirectory
from io import BytesIO
from pdf2image import convert_from_path
from pytesseract import pytesseract
from text_processing.correct_spelling import correct_spelling
from ocr_utils import setup_tesseract
from poppler_utils import setup_poppler
from pages.utils import convert_pdf_to_word
from pdf2docx import Converter

# Setup Poppler and Tesseract
setup_poppler()
setup_tesseract(['eng', 'ara', 'spa'])

def pdf_to_word(pdf_file):
    # Convert PDF file to Word
    word_file = BytesIO()
    with TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "temp.pdf")
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(pdf_file.read())
        cv = Converter(temp_file_path)
        cv.convert(word_file, start=0, end=None)
        cv.close()
    word_file.seek(0)
    return word_file

def show():
    st.title("🏠 Home")

    # Create a file uploader with drag-and-drop support
    uploaded_file = st.file_uploader("📂 Choose a PDF file or drag and drop here", type=["pdf"])

    # Create a selectbox for language
    language = st.selectbox("🌐 Select language", ["Automatic", "English", "Arabic", "Spanish"])

    # Define language codes
    lang_code = {
        'English': 'eng',
        'Arabic': 'ara',
        'Spanish': 'spa'
    }

    # Set default languages for 'Automatic'
    if language == 'Automatic':
        lang_codes = ['eng', 'ara']  # Default to English and Arabic
    else:
        lang_codes = [lang_code.get(language, '')]

    # Join lang_codes into a comma-separated string for pytesseract
    lang_codes_str = '+'.join(lang_codes)  # Changed from ',' to '+'

    def extract_text_from_image(image):
        return pytesseract.image_to_string(image, lang=lang_codes_str)

    # Create a page range input
    page_range = st.text_input("📄 Enter page range (e.g., 1-5 or 1,2,3)", value="")

    # Create a checkbox for spell checking
    spell_check = st.checkbox("🔍 Enable Spell Checking For English", value=True)

    # Create a checkbox to display images
    display_images = st.checkbox("🖼️ Display Images", value=False)

    # Create buttons for conversion options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🖼️ Convert PDF to Images and Extract Text"):
            if uploaded_file:
                with TemporaryDirectory() as temp_dir:
                    temp_file_path = os.path.join(temp_dir, "temp.pdf")
                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(uploaded_file.read())

                    try:
                        # Handle page range input
                        page_range_list = [int(x) for x in page_range.replace("-", ",").split(",")] if page_range else None
                        images = convert_from_path(temp_file_path, first_page=page_range_list[0], last_page=page_range_list[-1]) if page_range_list else convert_from_path(temp_file_path)

                        progress_bar = st.progress(0)  # شريط تقدم
                        time_bar = st.empty()
                        extracted_texts = []
                        total_pages = len(images)
                        start_time = time.time()

                        for i, image in enumerate(images):
                            progress_bar.progress((i + 1) / total_pages)
                            elapsed_time = time.time() - start_time
                            time_bar.info(f"⏱️ Time elapsed: {elapsed_time:.2f} seconds")
                            text = extract_text_from_image(image)

                            if spell_check and 'eng' in lang_codes:
                                text = correct_spelling(text, 'eng')
                            extracted_texts.append(text)

                        st.session_state['extracted_texts'] = extracted_texts
                        st.session_state['extracted_images'] = images
                        st.session_state['uploaded_filename'] = uploaded_file.name

                        if display_images:
                            for i, image in enumerate(images):
                                st.image(image, caption=f"Page {i + 1}")

                        st.success("✅ Conversion completed!")
                        progress_bar.empty()
                        time_bar.empty()

                    except Exception as e:
                        st.error(f"❌ An error occurred: {e}")
            else:
                st.error("⚠️ Please select a PDF file to convert")

    with col2:
        if st.button("📝 Convert PDF to Word"):
            if uploaded_file:
                try:
                    st.write("Processing...")
                    
                    start_time = time.time()
                    time_bar = st.empty()
                    
                    word_file = pdf_to_word(uploaded_file)
                    
                    elapsed_time = time.time() - start_time
                    time_bar.info(f"⏱️ Time elapsed: {elapsed_time:.2f} seconds")
                    
                    st.success("✅ Conversion completed!")
                    
                    st.download_button(
                        label="📥 Download Word Document",
                        data=word_file,
                        file_name="converted.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                except Exception as e:
                    st.error(f"❌ An error occurred during conversion: {str(e)}")
            else:
                st.error("⚠️ Please upload a PDF file.")


if __name__ == "__main__":
    show()