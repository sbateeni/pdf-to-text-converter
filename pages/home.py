import streamlit as st
import os
from tempfile import TemporaryDirectory, NamedTemporaryFile
from pdf2image import convert_from_path
from pytesseract import pytesseract
from text_processing.correct_spelling import correct_spelling
from ocr_utils import setup_tesseract
from poppler_utils import setup_poppler
from pages.utils import allowed_file, save_text_to_word, convert_pdf_to_word

# Setup Poppler and Tesseract
setup_poppler()
setup_tesseract(['eng', 'ara', 'spa'])

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
    lang_codes_str = ','.join(lang_codes)

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

                        progress_bar = st.progress(0)
                        extracted_texts = []
                        total_pages = len(images)

                        for i, image in enumerate(images):
                            progress_bar.progress((i + 1) / total_pages)
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

                    except Exception as e:
                        st.error(f"❌ An error occurred: {e}")
            else:
                st.error("⚠️ Please select a PDF file to convert")

    with col2:
        if st.button("📝 Convert PDF to Word"):
            if uploaded_file:
                if allowed_file(uploaded_file.name):
                    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                        temp_file.write(uploaded_file.read())
                        temp_file_path = temp_file.name

                    word_filename = uploaded_file.name.rsplit('.', 1)[0] + '.docx'
                    word_file_path = os.path.join('downloads', word_filename)
                    os.makedirs('downloads', exist_ok=True)

                    try:
                        convert_pdf_to_word(temp_file_path, 'downloads')
                        st.success("✅ Conversion completed!")

                        with open(word_file_path, "rb") as f:
                            st.download_button(
                                label="📥 Download Word File",
                                data=f,
                                file_name=os.path.basename(word_file_path)
                            )
                    except Exception as e:
                        st.error(f"❌ An error occurred: {e}")
                else:
                    st.error("⚠️ Invalid file format. Please upload a PDF file.")
            else:
                st.error("⚠️ Please upload a PDF file.")
