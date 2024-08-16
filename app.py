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
from fpdf import FPDF

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

# Create a text input for searching text
search_query = st.text_input("Search text in extracted content")

# Function to extract text from images
def extract_text_from_images(images, lang_code, spell_check):
    extracted_texts = []
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang=lang_code)
        if spell_check and lang_code == 'eng':
            text = correct_spelling(text, lang_code)
        extracted_texts.append(text)
    return extracted_texts

# Function to display extracted text
def display_extracted_text(extracted_texts):
    for i, text in enumerate(extracted_texts):
        st.markdown(f"### Page {i + 1}:")
        markdown_text = markdown.markdown(text)
        st.markdown(markdown_text, unsafe_allow_html=True)

# Function to handle search
def handle_search(search_query, extracted_texts):
    st.markdown("## Search Results")
    for i, text in enumerate(extracted_texts):
        if search_query.lower() in text.lower():
            st.markdown(f"### Page {i + 1}:")
            highlighted_text = text.replace(search_query, f"**{search_query}**")
            st.markdown(markdown.markdown(highlighted_text), unsafe_allow_html=True)

# Function to save and download text files
def save_and_download_text_file(file_type, extracted_texts, uploaded_filename):
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

def save_text_to_pdf(extracted_texts, uploaded_filename):
    # Create a PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for text in extracted_texts:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        try:
            # Ensure text is encoded in utf-8
            pdf.multi_cell(0, 10, text.encode('latin1', 'replace').decode('latin1'))
        except UnicodeEncodeError:
            # If encoding fails, fallback to utf-8
            pdf.multi_cell(0, 10, text.encode('utf-8').decode('utf-8'))

    # Save the PDF with the original filename but as a PDF
    pdf_file_path = uploaded_filename.replace(".pdf", "_converted.pdf")
    pdf.output(pdf_file_path)

    return pdf_file_path

# Main Convert button action
if st.button("Convert"):
    if uploaded_file:
        with TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "temp.pdf")
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.read())

            try:
                page_range = [int(x) for x in page_range.replace("-", ",").split(",")] if page_range else None
                images = convert_from_path(temp_file_path, first_page=page_range[0],
                                           last_page=page_range[-1]) if page_range else convert_from_path(
                    temp_file_path)

                progress_bar = st.progress(0)
                total_pages = len(images)

                extracted_texts = extract_text_from_images(images, lang_code, spell_check)

                # Save extracted text to session state
                st.session_state['extracted_texts'] = extracted_texts
                st.session_state['uploaded_filename'] = uploaded_file.name

                if display_images:
                    for i, image in enumerate(images):
                        st.image(image, caption=f"Page {i + 1}")

                display_extracted_text(extracted_texts)
                progress_bar.progress(100)

                if search_query:
                    handle_search(search_query, extracted_texts)

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
