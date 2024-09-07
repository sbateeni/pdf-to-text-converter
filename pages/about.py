import streamlit as st

def show():
    st.title("📖 About This Project")
    st.markdown("""
    This project is a PDF to text converter that allows users to convert PDF files to images, extract text, and save it in various formats.
    
    ## Features
    - Convert PDF pages to images
    - Extract text using OCR
    - Convert extracted text to speech
    - Save extracted text to Word or Markdown

    ## Contact
    For any questions or issues, please contact [Your Name](mailto:your.email@example.com).
    """)

if __name__ == "__main__":
    show()