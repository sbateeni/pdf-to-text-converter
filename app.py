import streamlit as st

# Streamlit app setup
st.title("📄✨ PDF Converter and Text Extractor")
st.markdown("Convert PDF files to images, extract text, and convert to Word.")

# Sidebar for navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Text Search", "Image Viewer", "HTML to Word", "Image to PDF"])

# Load the corresponding page based on the selection
if page == "Home":
    from pages import home
    home.show()

elif page == "Text Search":
    from pages import text_search
    text_search.show()

elif page == "Image Viewer":
    from pages import image_viewer
    image_viewer.show()

elif page == "HTML to Word":
    from pages import html_to_word
    html_to_word.show()

elif page == "Image to PDF":
    from pages import image_to_pdf
    image_to_pdf.show()
