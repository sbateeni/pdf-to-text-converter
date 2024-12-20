import streamlit as st
from utils.text_processing import format_text
from utils.pdf_processing import extract_text_from_pdf, perform_ocr, convert_pdf_to_images_and_text
from utils.file_handling import create_docx, format_output, save_uploaded_file
from ui.components import (
    init_session_state,
    create_sidebar,
    create_processing_tabs,
    display_results,
    apply_theme
)

# Set up page config
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
    
    st.write("قم بتحميل ملف PDF وتحويله إلى نص مع دعم للغات المتعددة")

    # File upload
    uploaded_file = st.file_uploader("اختر ملف PDF", type="pdf")
    
    if uploaded_file is not None:
        # Save uploaded file and store path
        pdf_path = save_uploaded_file(uploaded_file)
        st.session_state.current_pdf_path = pdf_path
        
        # Show processing options
        create_processing_tabs()
    else:
        st.session_state.current_pdf_path = None
        st.info("الرجاء تحميل ملف PDF للبدء")

if __name__ == "__main__":
    main()