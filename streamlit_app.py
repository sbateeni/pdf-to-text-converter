import streamlit as st
import tempfile
from pathlib import Path
import logging
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils.text_processing import format_text
from src.utils.pdf_processing import extract_text_from_pdf, perform_ocr, convert_pdf_to_images_and_text
from src.utils.file_handling import create_docx, format_output, save_uploaded_file
from src.ui.components import (
    init_session_state,
    create_sidebar,
    create_processing_tabs,
    display_results
)

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

def main():
    # Initialize session state
    init_session_state()
    
    # Apply theme
    apply_theme()
    
    st.title("PDF to Text Converter")
    
    # Create sidebar
    create_sidebar()
    
    st.write("Upload your PDF file and convert it to text with support for multiple languages")

    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        pdf_path = save_uploaded_file(uploaded_file)
        
        # Get total pages
        _, total_pages, _ = extract_text_from_pdf(str(pdf_path), detect_lang=False)
        
        # Page selection
        st.subheader("Page Selection")
        process_all_pages = st.checkbox("Process all pages", value=True)
        
        if not process_all_pages:
            page_range = st.text_input(
                "Enter page range (e.g., 1-3 or 1,2,3 or 1-3,5-7)",
                value="1"
            )
        else:
            page_range = None

        # Processing options
        st.subheader("Processing Options")
        create_processing_tabs()
        
        # Preview option
        preview_pdf = st.checkbox("Preview PDF", value=False)

        # نقل خيار طريقة المعالجة إلى الصفحة الرئيسية
        st.subheader("طريقة المعالجة")
        processing_method = st.radio(
            "اختر طريقة تحويل PDF",
            ["تحويل مباشر", "تحويل عبر الصور"],
            horizontal=True,
            help="""
            - تحويل مباشر: استخراج النص مباشرة من PDF
            - تحويل عبر الصور: تحويل PDF إلى صور ثم استخراج النص منها (مفيد عندما يفشل التحويل المباشر)
            """
        )

        if st.button("معالجة PDF", type="primary"):
            try:
                with st.spinner("Processing PDF..."):
                    # Get settings from session state
                    settings = st.session_state.settings
                    
                    # Preview PDF if requested
                    if preview_pdf:
                        from pdf2image import convert_from_path
                        images = convert_from_path(str(pdf_path))
                        st.subheader("PDF Preview")
                        
                        # Get pages to preview
                        if page_range:
                            from src.utils.pdf_processing import parse_page_range
                            preview_pages = parse_page_range(page_range, len(images))
                            for page_num in preview_pages:
                                st.image(images[page_num], caption=f"Page {page_num + 1}")
                        else:
                            for i, image in enumerate(images):
                                st.image(image, caption=f"Page {i + 1}")

                    if processing_method == "تحويل مباشر":
                        # Extract text
                        if settings['use_ocr']:
                            text, page_languages = perform_ocr(
                                str(pdf_path),
                                page_range=page_range,
                                detect_lang=settings['auto_detect_lang'],
                                manual_langs=settings['manual_langs'],
                                enhance_images=settings['enhance_images']
                            )
                        else:
                            text, _, page_languages = extract_text_from_pdf(
                                str(pdf_path),
                                page_range=page_range,
                                detect_lang=settings['auto_detect_lang'],
                                manual_langs=settings['manual_langs']
                            )
                    else:
                        # التحويل عبر الصور
                        text, total_pages, page_languages, processed_pages = convert_pdf_to_images_and_text(
                            pdf_path,
                            page_range=page_range,
                            languages=settings['manual_langs'] if not settings['auto_detect_lang'] else None
                        )
                        # عرض الصور المحولة
                        st.subheader("الصور المستخرجة")
                        image_cols = st.columns(3)
                        for i, page_num in enumerate(processed_pages):
                            image_path = f"{pdf_path}_page_{page_num + 1}.png"
                            with image_cols[i % 3]:
                                st.image(image_path, caption=f"صفحة {page_num + 1}", use_column_width=True)

                    # Format text
                    text = format_text(text, {
                        'line_spacing': settings['line_spacing'],
                        'margins': settings['add_margins']
                    })
                    
                    # Remove extra spaces if requested
                    if settings['remove_extra_spaces']:
                        text = " ".join(text.split())

                    # Create metadata for output
                    metadata = {
                        'Total Pages': total_pages,
                        'Processed Pages': page_range if page_range else 'All',
                        'OCR Used': 'Yes' if settings['use_ocr'] else 'No',
                        'Languages Detected': ', '.join(set(sum(page_languages.values(), []))) if page_languages else 'N/A'
                    }

                    # Format output based on selected format
                    output_text = format_output(text, settings['output_format'], metadata)

                    # Display results
                    st.subheader("Extracted Text")
                    st.text_area("", output_text, height=300)

                    # Prepare download buttons
                    if settings['output_format'] == 'docx':
                        docx_path = Path(tempfile.gettempdir()) / "output.docx"
                        create_docx(output_text, str(docx_path))
                        
                        with open(docx_path, "rb") as docx_file:
                            st.download_button(
                                label="Download DOCX",
                                data=docx_file,
                                file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                    else:
                        # Download text in selected format
                        extension = settings['output_format']
                        mime_type = {
                            'txt': 'text/plain',
                            'md': 'text/markdown',
                            'html': 'text/html'
                        }[settings['output_format']]
                        
                        st.download_button(
                            label=f"Download {settings['output_format'].upper()}",
                            data=output_text,
                            file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.{extension}",
                            mime=mime_type
                        )

            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
                logger.error(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    main()