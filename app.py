import streamlit as st
import tempfile
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

# Setup Poppler and Tesseract
setup_poppler()
setup_tesseract(['eng', 'ara', 'spa'])

# Set up the app title and header
st.title("PDF to Image Converter")
st.header("Convert PDF files to images and extract text")

# Create a file uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# Create a selectbox for language
language = st.selectbox("Select language", ["English", "Arabic", "Spanish"])
lang_code = {'English': 'eng', 'Arabic': 'ara', 'Spanish': 'spa'}[language]

# Create a page range input
page_range = st.text_input("Enter page range (e.g. 1-5 or 1,2,3)", value="")

# Create a checkbox for spell checking
spell_check = st.checkbox("Enable Spell Checking For English", value=False)

# Create a checkbox to display images
display_images = st.checkbox("Display Images", value=True)

# Create a text input for searching text
search_query = st.text_input("Search text in extracted content")

# Create a button to trigger the conversion
if st.button("Convert"):
    if uploaded_file is not None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "temp.pdf")
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.getvalue())

            try:
                if page_range:
                    page_range = [int(x) for x in page_range.replace("-", ",").split(",")]
                    images = convert_from_path(temp_file_path, first_page=page_range[0], last_page=page_range[-1])
                else:
                    images = convert_from_path(temp_file_path)

                progress_bar = st.progress(0)
                total_pages = len(images)
                extracted_texts = []

                for i, image in enumerate(images):
                    if display_images:
                        st.image(image, caption=f"Page {i + 1}")

                    text = pytesseract.image_to_string(image, lang=lang_code)
                    if spell_check:
                        text = correct_spelling(text, lang_code)
                    markdown_text = markdown.markdown(text)

                    st.write(f"### Page {i + 1}:")
                    st.write(markdown_text, unsafe_allow_html=True)

                    extracted_texts.append(text)

                    progress_bar.progress((i + 1) / total_pages)

                # Create a button to search the text in extracted content
                if st.button("Search Text"):
                    st.header("Search Results")
                    for i, text in enumerate(extracted_texts):
                        if search_query.lower() in text.lower():
                            st.write(f"### Page {i + 1}:")
                            highlighted_text = text.replace(search_query, f"**{search_query}**")
                            st.write(markdown.markdown(highlighted_text), unsafe_allow_html=True)

                # Add a button to save the text to Word
                if st.button("Save Text to Word"):
                    pdf_filename = uploaded_file.name
                    word_file = save_text_to_word(extracted_texts, pdf_filename)
                    with open(word_file, "rb") as f:
                        st.download_button(label="Download Word File", data=f, file_name=os.path.basename(word_file))

                # Add a button to save the text to PDF
                if st.button("Save Text to PDF"):
                    pdf_filename = uploaded_file.name
                    pdf_file = save_text_to_pdf(extracted_texts, pdf_filename)
                    if pdf_file:
                        with open(pdf_file, "rb") as f:
                            st.download_button(label="Download PDF File", data=f, file_name=os.path.basename(pdf_file))

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.error("Please select a PDF file to convert")

# Create a button to clear the search query
if st.button("Clear Search Query"):
    search_query = ""
    st.experimental_rerun()
