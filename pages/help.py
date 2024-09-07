import streamlit as st

def show():
    st.title("❓ Help")
    st.markdown("""
    ## How to Use This Application

    1. **Upload a PDF File**: Use the file uploader to select a PDF file.
    2. **Extract Text**: Click on the "Convert" button to extract text from the PDF.
    3. **Search Text**: Navigate to the "Text Search" page to search for specific terms in the extracted text.
    4. **Convert to Word**: Save the extracted text to a Word document using the provided button.
    """)

if __name__ == "__main__":
    show()