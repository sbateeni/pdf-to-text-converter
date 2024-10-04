import streamlit as st
from utils import get_translation

def show():
    language = st.session_state.language
    st.title(get_translation("Help", language))

    st.markdown(get_translation("Welcome to the PDF Converter and Text Extractor help page!", language))

    st.header(get_translation("General Usage", language))
    st.markdown(get_translation("""
    1. Use the sidebar to navigate between different tools and features.
    2. Each page provides specific instructions for its functionality.
    3. You can change the language using the language selector in the sidebar.
    """, language))

    st.header(get_translation("Available Tools", language))
    tools = [
        "GROQ PDF Merge", "Text Search", "Image Viewer", "HTML to Word",
        "Image to PDF", "Convert Image to Text", "Word to PDF", "Excel to PDF",
        "CSV to Excel", "JSON to CSV", "XML to JSON", "TXT to PDF",
        "PPTX to PDF", "PDF to Images", "HTML to Markdown", "YAML to JSON",
        "RTF to PDF"
    ]

    for tool in tools:
        st.markdown(f"- {get_translation(tool, language)}")

    st.header(get_translation("GROQ API Usage", language))
    st.markdown(get_translation("""
    To use the GROQ PDF Merge feature:
    1. Enter your GROQ API key on the GROQ PDF Merge page.
    2. Upload your PDF file.
    3. The app will extract text from the PDF and send it to the GROQ API for processing.
    4. View the results returned by the API.
    """, language))

    st.header(get_translation("Troubleshooting", language))
    st.markdown(get_translation("""
    - If you encounter any errors, check the Error Log page for more details.
    - Make sure you have a stable internet connection when using online features.
    - Ensure your API key is entered correctly for GROQ-related features.
    - If a file fails to upload or process, try a different file format or a smaller file size.
    """, language))

    st.header(get_translation("Contact Support", language))
    st.markdown(get_translation("""
    If you need further assistance, please contact our support team at support@pdfconverter.com
    """, language))

if __name__ == "__main__":
    show()