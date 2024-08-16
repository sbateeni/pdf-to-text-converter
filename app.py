import streamlit as st
from tempfile import TemporaryDirectory
import os
import re
from pdf2image import convert_from_path
from pytesseract import pytesseract
from PIL import Image
from ocr_utils import setup_tesseract
from poppler_utils import setup_poppler
from text_processing.correct_spelling import correct_spelling
from file_handling.save_text_to_word import save_text_to_word
from file_handling.save_text_to_pdf import save_text_to_pdf

# Setup Poppler and Tesseract
setup_poppler()
setup_tesseract(['eng', 'ara', 'spa'])

# Streamlit app setup
st.title("PDF to Image Converter")
st.markdown("Convert PDF files to images and extract text")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Converter", "Text Search"])

# Initialize session state for images and text
if 'extracted_images' not in st.session_state:
    st.session_state['extracted_images'] = []
if 'extracted_texts' not in st.session_state:
    st.session_state['extracted_texts'] = []

if page == "Converter":
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

    if st.button("Convert"):
        if uploaded_file:
            with TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, "temp.pdf")
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(uploaded_file.read())

                try:
                    page_range = [int(x) for x in page_range.replace("-", ",").split(",")] if page_range else None
                    images = convert_from_path(temp_file_path, first_page=page_range[0],
                                               last_page=page_range[-1]) if page_range else convert_from_path(temp_file_path)

                    # Initialize progress bar
                    progress_bar = st.progress(0)
                    extracted_texts = []
                    total_pages = len(images)

                    for i, image in enumerate(images):
                        # Update progress bar
                        progress_bar.progress((i + 1) / total_pages)

                        text = pytesseract.image_to_string(image, lang=lang_code)
                        if spell_check and lang_code == 'eng':
                            text = correct_spelling(text, lang_code)
                        extracted_texts.append(text)

                    # Store extracted texts and images in session state
                    st.session_state['extracted_texts'] = extracted_texts
                    st.session_state['extracted_images'] = images
                    st.session_state['uploaded_filename'] = uploaded_file.name

                    if display_images:
                        for i, image in enumerate(images):
                            st.image(image, caption=f"Page {i + 1}")

                    st.success("Conversion completed!")
                    progress_bar.empty()

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please select a PDF file to convert")

    # Add save buttons
    if st.session_state['extracted_texts']:
        st.markdown("### Save Extracted Text")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Text to Word"):
                word_file_path = save_text_to_word(st.session_state['extracted_texts'], st.session_state['uploaded_filename'])
                with open(word_file_path, "rb") as f:
                    st.download_button(
                        label="Download Word File",
                        data=f,
                        file_name=os.path.basename(word_file_path)
                    )
        with col2:
            if st.button("Save Text to PDF"):
                pdf_file_path = save_text_to_pdf(st.session_state['extracted_texts'], st.session_state['uploaded_filename'])
                with open(pdf_file_path, "rb") as f:
                    st.download_button(
                        label="Download PDF File",
                        data=f,
                        file_name=os.path.basename(pdf_file_path)
                    )

elif page == "Text Search":
    st.title("Text Search in Extracted Content")

    # Search functionality at the top
    search_query = st.text_input("Search text in extracted content", value="", placeholder="Type to search...")

    # Display the number of found words
    if search_query and st.session_state['extracted_texts']:
        word_count = 0
        for text in st.session_state['extracted_texts']:
            word_count += len(re.findall(re.escape(search_query), text, re.IGNORECASE))
        st.write(f"Number of occurrences of the search query: {word_count}")

    # Button to display extracted text
    if st.session_state['extracted_texts']:
        if st.button("Show Extracted Texts"):
            for i, text in enumerate(st.session_state['extracted_texts']):
                st.markdown(f"### Page {i + 1}")
                st.write(text)
    else:
        st.error("No text available. Please convert a PDF first.")

    if search_query:
        st.markdown(f"### Search Results for: `{search_query}`")
        for i, text in enumerate(st.session_state['extracted_texts']):
            if search_query.lower() in text.lower():
                highlighted_text = re.sub(f"(?i){search_query}", f"<span style='background-color: yellow;'>{search_query}</span>", text)
                st.markdown(f"#### Page {i + 1}:")
                st.markdown(highlighted_text, unsafe_allow_html=True)

    # Add button to clear text
    if st.button("Clear Text"):
        st.session_state['extracted_texts'] = []
        st.session_state['extracted_images'] = []
        st.success("Text has been cleared.")
