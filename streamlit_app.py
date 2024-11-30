import streamlit as st
import os
from utils import setup_logging
from file_handling.file_processor import process_file
from text_processing.text_processor import process_text
import tempfile

# Set up page config
st.set_page_config(
    page_title="PDF to Text Converter",
    page_icon="📄",
    layout="wide"
)

# Initialize logging
setup_logging()

def main():
    st.title("PDF to Text Converter")
    st.write("Upload your PDF file and convert it to text")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

    if uploaded_file is not None:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            # Process the file
            with st.spinner('Converting PDF to text...'):
                text = process_file(tmp_file_path)
                processed_text = process_text(text)

            # Display results
            st.subheader("Extracted Text:")
            st.text_area("", processed_text, height=300)

            # Download button for text
            st.download_button(
                label="Download Text",
                data=processed_text,
                file_name="converted_text.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

if __name__ == "__main__":
    main() 