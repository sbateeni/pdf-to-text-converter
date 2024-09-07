import streamlit as st
from pdf2image import convert_from_path
import tempfile

def convert_pdf_to_images(pdf_file):
    """Convert PDF file to images."""
    images = convert_from_path(pdf_file)
    return images

def show():
    st.title("📄 Convert PDF to Images")

    uploaded_file = st.file_uploader("📂 Choose a PDF file", type=["pdf"])

    if uploaded_file:
        if st.button("🖼️ Convert PDF to Images"):
            try:
                images = convert_pdf_to_images(uploaded_file)
                st.success("✅ Conversion completed!")

                for i, image in enumerate(images):
                    st.image(image, caption=f"Page {i + 1}")
            except Exception as e:
                st.error(f"❌ An error occurred during conversion: {str(e)}")

if __name__ == "__main__":
    show()