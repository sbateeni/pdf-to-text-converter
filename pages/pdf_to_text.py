import streamlit as st
import fitz  # PyMuPDF

def convert_pdf_to_text(pdf_file):
    """Convert PDF file to text."""
    text = ""
    with fitz.open(pdf_file) as doc:
        for page in doc:
            text += page.get_text()
    return text

def show():
    st.title("📄 Convert PDF to Text")

    uploaded_file = st.file_uploader("📂 Choose a PDF file", type=["pdf"])

    if uploaded_file:
        if st.button("📝 Convert PDF to Text"):
            try:
                text = convert_pdf_to_text(uploaded_file)
                st.success("✅ Conversion completed!")
                st.text_area("Extracted Text", text, height=300)
            except Exception as e:
                st.error(f"❌ An error occurred during conversion: {str(e)}")

if __name__ == "__main__":
    show()