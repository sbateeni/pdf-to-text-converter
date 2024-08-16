import streamlit as st
from tempfile import TemporaryDirectory
import os
import markdown
from pdf2image import convert_from_path
from pytesseract import pytesseract
from PIL import Image
from ocr_utils import setup_tesseract
from poppler_utils import setup_poppler
from text_processing.reverse_text import reverse_text
from text_processing.correct_spelling import correct_spelling
from file_handling.save_text_to_word import save_text_to_word
from file_handling.save_text_to_pdf import save_text_to_pdf
import re

# Setup Poppler and Tesseract
setup_poppler()
setup_tesseract(['eng', 'ara', 'spa'])

# Streamlit app setup
st.title("PDF to Image Converter")
st.markdown("Convert PDF files to images and extract text")

# Create a file uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# Create a selectbox for language
language = st.selectbox("Select language", ["English", "Arabic", "Spanish"])
lang_code = {'English': 'eng', 'Arabic': 'ara', 'Spanish': 'spa'}[language]

# Create a page range input
page_range = st.text_input("Enter page range (e.g., 1-5 or 1,2,3)", value="")

# Create a checkbox for spell checking
spell_check = st.checkbox("Enable Spell Checking For English", value=False)

# Create a checkbox to display images
display_images = st.checkbox("Display Images", value=True)

# Create a text input for searching text with automatic search
search_query = st.text_input("Search text in extracted content", value="", placeholder="Type to search...")

def extract_text_from_images(images, lang_code, spell_check):
    extracted_texts = []
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang=lang_code)
        if spell_check and lang_code == 'eng':
            text = correct_spelling(text, lang_code)
        extracted_texts.append(text)
    return extracted_texts

def display_extracted_text(extracted_texts, search_query=""):
    for i, text in enumerate(extracted_texts):
        st.markdown(f"### Page {i + 1}:")
        if search_query:
            # Highlight search query in the text with yellow background
            highlighted_text = re.sub(
                re.escape(search_query),
                lambda m: f'<span style="background-color: yellow;">{m.group(0)}</span>',
                text,
                flags=re.IGNORECASE
            )
            st.markdown(f'<div>{highlighted_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(text)

def save_and_download_text_file(file_type, extracted_texts, uploaded_filename):
    file_path = None
    if file_type == "Word":
        file_path = save_text_to_word(extracted_texts, uploaded_filename)
    elif file_type == "PDF":
        file_path = save_text_to_pdf(extracted_texts, uploaded_filename)

    if file_path:
        with open(file_path, "rb") as f:
            st.download_button(
                label=f"Download {file_type} File",
                data=f,
                file_name=os.path.basename(file_path)
            )

if st.button("Convert"):
    if uploaded_file:
        with TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "temp.pdf")
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.read())

            try:
                page_range_list = [int(x) for x in page_range.replace("-", ",").split(",")] if page_range else None
                images = convert_from_path(temp_file_path, first_page=page_range_list[0] if page_range_list else None,
                                           last_page=page_range_list[-1] if page_range_list else None)

                progress_bar = st.progress(0)
                total_pages = len(images)

                extracted_texts = extract_text_from_images(images, lang_code, spell_check)

                # Save extracted text to session state
                st.session_state['extracted_texts'] = extracted_texts
                st.session_state['uploaded_filename'] = uploaded_file.name

                if display_images:
                    for i, image in enumerate(images):
                        st.image(image, caption=f"Page {i + 1}")

                # Display extracted text with search highlighting
                display_extracted_text(extracted_texts, search_query)
                progress_bar.progress(100)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please select a PDF file to convert")

# Button actions for saving text to Word or PDF
if 'extracted_texts' in st.session_state:
    if st.button("Save Text to Word"):
        save_and_download_text_file("Word", st.session_state['extracted_texts'], st.session_state['uploaded_filename'])

    if st.button("Save Text to PDF"):
        save_and_download_text_file("PDF", st.session_state['extracted_texts'], st.session_state['uploaded_filename'])

# Automatically update search results as the user types
if 'extracted_texts' in st.session_state:
    display_extracted_text(st.session_state['extracted_texts'], search_query)
