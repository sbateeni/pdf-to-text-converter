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
from pdf2docx import Converter
import docx
from langdetect import detect
import cv2
import numpy as np
from mdutils.mdutils import MdUtils
from htmldocx import HtmlToDocx

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set theme
st.set_page_config(
    page_title="PDF to Text Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme settings
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

def apply_theme():
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stTextInput, .stSelectbox, .stMultiselect {
            background-color: #2D2D2D;
            color: #FFFFFF;
        }
        </style>
        """, unsafe_allow_html=True)

def detect_language(text):
    """Detect the language of the text"""
    try:
        lang = detect(text)
        lang_map = {
            'en': 'eng',
            'ar': 'ara',
            'es': 'spa'
        }
        return lang_map.get(lang, 'eng')
    except:
        return 'eng'

def enhance_image(image):
    """Enhance image quality for better OCR"""
    try:
        # Convert PIL Image to OpenCV format
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Apply image preprocessing
        # 1. Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 2. Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # 3. Denoise
        denoised = cv2.fastNlMeansDenoising(binary)
        
        # Convert back to PIL Image
        enhanced = Image.fromarray(denoised)
        return enhanced
    except Exception as e:
        logger.error(f"Error enhancing image: {str(e)}")
        return image

def format_text(text, format_options):
    """Format text based on selected options"""
    try:
        # Apply line spacing
        if format_options.get('line_spacing'):
            text = '\n'.join([line + '\n' for line in text.split('\n')])
            
        # Apply margins
        if format_options.get('margins'):
            text = '\n'.join(['    ' + line for line in text.split('\n')])
            
        # Convert to selected format
        output_format = format_options.get('output_format', 'txt')
        if output_format == 'md':
            md = MdUtils(file_name='output')
            md.new_header(1, "Extracted Text")
            md.new_paragraph(text)
            return md.get_md_text()
        elif output_format == 'html':
            return f"<html><body><pre>{text}</pre></body></html>"
        
        return text
    except Exception as e:
        logger.error(f"Error formatting text: {str(e)}")
        return text

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

def extract_text_from_pdf(pdf_path, page_numbers=None):
    """Extract text from PDF using PyPDF2"""
    try:
        text = ""
        pdf_reader = PdfReader(pdf_path)
        total_pages = len(pdf_reader.pages)
        
        # If no specific pages are selected, process all pages
        if not page_numbers:
            page_numbers = list(range(total_pages))
        
        # Validate page numbers
        page_numbers = [p for p in page_numbers if 0 <= p < total_pages]
        
        for page_num in page_numbers:
            text += f"\n--- Page {page_num + 1} ---\n"
            text += pdf_reader.pages[page_num].extract_text() + "\n"
        return text.strip(), total_pages
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def perform_ocr(pdf_path, lang='eng', page_numbers=None):
    """Perform OCR on PDF pages"""
    try:
        text = ""
        images = convert_from_path(pdf_path)
        total_pages = len(images)
        
        # If no specific pages are selected, process all pages
        if not page_numbers:
            page_numbers = list(range(total_pages))
            
        # Validate page numbers
        page_numbers = [p for p in page_numbers if 0 <= p < total_pages]
        
        for page_num in page_numbers:
            text += f"\n--- Page {page_num + 1} ---\n"
            text += pytesseract.image_to_string(images[page_num], lang=lang) + "\n"
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

def convert_to_docx(pdf_path, output_path, page_numbers=None):
    """Convert PDF to DOCX format"""
    try:
        cv = Converter(pdf_path)
        if page_numbers:
            cv.convert(output_path, pages=page_numbers)
        else:
            cv.convert(output_path)
        cv.close()
        return True
    except Exception as e:
        logger.error(f"Error converting to DOCX: {str(e)}")
        raise

def main():
    # Apply theme
    apply_theme()
    
    st.title("PDF to Text Converter")
    
    # Create sidebar with navigation and theme toggle
    with st.sidebar:
        st.title("Navigation")
        st.write("Additional Tools:")
        st.page_link("pages/1_🔍_OCR.py", label="OCR Processing", icon="🔍")
        st.page_link("pages/2_📝_Text_Editor.py", label="Text Editor", icon="📝")
        st.page_link("pages/3_📊_Text_Analysis.py", label="Text Analysis", icon="📊")
        
        st.divider()
        st.write("Settings:")
        theme_toggle = st.button(
            "Toggle Dark/Light Theme",
            on_click=toggle_theme
        )
    
    st.write("Upload your PDF file and convert it to text with support for multiple languages")

    # Check dependencies
    if not check_dependencies():
        st.error("Some required dependencies are not available. Please check the logs for details.")
        return

    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Save uploaded file temporarily to get page count
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "temp.pdf"
            pdf_path.write_bytes(uploaded_file.getvalue())
            
            # Get total pages
            _, total_pages = extract_text_from_pdf(str(pdf_path))
            
            # Page selection
            st.subheader("Page Selection")
            process_all_pages = st.checkbox("Process all pages", value=True)
            
            if not process_all_pages:
                page_numbers = st.multiselect(
                    "Select pages to process",
                    options=list(range(1, total_pages + 1)),
                    default=[1]
                )
                # Convert to 0-based index
                selected_pages = [p - 1 for p in page_numbers]
            else:
                selected_pages = None

            # Processing options
            st.subheader("Processing Options")
            
            # Create tabs for different settings
            tabs = st.tabs(["OCR & Language", "Image Enhancement", "Text Formatting"])
            
            with tabs[0]:
                col1, col2 = st.columns(2)
                with col1:
                    use_ocr = st.checkbox("Use OCR", value=True)
                    auto_detect_lang = st.checkbox("Auto-detect language", value=True)
                with col2:
                    lang = st.selectbox(
                        "Select document language",
                        options=['eng', 'ara', 'spa'],
                        format_func=lambda x: {'eng': 'English', 'ara': 'Arabic', 'spa': 'Spanish'}[x],
                        disabled=auto_detect_lang
                    )
            
            with tabs[1]:
                col1, col2 = st.columns(2)
                with col1:
                    enhance_images = st.checkbox("Enhance image quality", value=True)
                    preview_enhanced = st.checkbox("Preview enhanced images", value=False)
                with col2:
                    correct_spelling = st.checkbox("Correct spelling", value=True)
                    remove_extra_spaces = st.checkbox("Remove extra spaces", value=True)
            
            with tabs[2]:
                col1, col2 = st.columns(2)
                with col1:
                    line_spacing = st.checkbox("Double line spacing", value=False)
                    add_margins = st.checkbox("Add margins", value=False)
                with col2:
                    output_format = st.selectbox(
                        "Output format",
                        options=['txt', 'md', 'html', 'docx'],
                        format_func=lambda x: {
                            'txt': 'Plain Text',
                            'md': 'Markdown',
                            'html': 'HTML',
                            'docx': 'Word Document'
                        }[x]
                    )
            
            # Preview option
            preview_pdf = st.checkbox("Preview PDF", value=False)

            if st.button("Process PDF"):
                with st.spinner("Processing PDF..."):
                    try:
                        # Preview PDF if requested
                        if preview_pdf:
                            images = convert_from_path(str(pdf_path))
                            st.subheader("PDF Preview")
                            if selected_pages:
                                for page_num in selected_pages:
                                    st.image(images[page_num], caption=f"Page {page_num + 1}")
                            else:
                                for i, image in enumerate(images):
                                    st.image(image, caption=f"Page {i + 1}")

                        # Extract text
                        if use_ocr:
                            # Convert PDF to images
                            images = convert_from_path(str(pdf_path))
                            text = ""
                            
                            # Process selected pages
                            pages_to_process = selected_pages if selected_pages else range(len(images))
                            
                            for page_num in pages_to_process:
                                # Enhance image if requested
                                image = images[page_num]
                                if enhance_images:
                                    image = enhance_image(image)
                                    if preview_enhanced:
                                        st.image(image, caption=f"Enhanced Page {page_num + 1}")
                                
                                # Perform OCR
                                page_text = pytesseract.image_to_string(image)
                                
                                # Auto-detect language if enabled
                                if auto_detect_lang:
                                    lang = detect_language(page_text)
                                
                                text += f"\n--- Page {page_num + 1} ---\n"
                                text += pytesseract.image_to_string(image, lang=lang) + "\n"
                        else:
                            text, _ = extract_text_from_pdf(str(pdf_path), selected_pages)

                        # Post-process text
                        if correct_spelling:
                            text = correct_text(text, lang)
                        if remove_extra_spaces:
                            text = " ".join(text.split())

                        # Format text
                        text = format_text(text, {
                            'line_spacing': line_spacing,
                            'margins': add_margins,
                            'output_format': output_format
                        })

                        # Display results
                        st.subheader("Extracted Text")
                        st.text_area("", text, height=300)

                        # Prepare download buttons
                        if output_format == 'docx':
                            docx_path = Path(temp_dir) / "output.docx"
                            if output_format == 'html':
                                # Convert HTML to DOCX
                                parser = HtmlToDocx()
                                parser.parse_html_string(text, docx_path)
                            else:
                                # Create DOCX from text
                                doc = docx.Document()
                                doc.add_paragraph(text)
                                doc.save(docx_path)
                            
                            with open(docx_path, "rb") as docx_file:
                                st.download_button(
                                    label="Download DOCX",
                                    data=docx_file,
                                    file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                        else:
                            # Download text in selected format
                            extension = output_format
                            mime_type = {
                                'txt': 'text/plain',
                                'md': 'text/markdown',
                                'html': 'text/html'
                            }[output_format]
                            
                            st.download_button(
                                label=f"Download {output_format.upper()}",
                                data=text,
                                file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.{extension}",
                                mime=mime_type
                            )

                    except Exception as e:
                        st.error(f"Error processing PDF: {str(e)}")
                        logger.error(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    main()