import streamlit as st

# Streamlit app setup
st.title("📄✨ PDF Converter and Text Extractor")
st.markdown("Convert PDF files to images, extract text, and convert to Word.")

# Sidebar for navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Text Search", "Image Viewer", "HTML to Word", "Image to PDF", "Convert Image to Text"])

# Load the corresponding page based on the selection
if page == "Home":
    from pages.home import show as home_show
    home_show()

elif page == "Text Search":
    from pages.text_search import show as text_search_show
    text_search_show()

elif page == "Image Viewer":
    from pages.image_viewer import show as image_viewer_show
    image_viewer_show()

elif page == "HTML to Word":
    from pages.html_to_word import show as html_to_word_show
    html_to_word_show()

elif page == "Image to PDF":
    from pages.image_to_pdf import show as image_to_pdf_show
    image_to_pdf_show()

elif page == "Convert Image to Text":
    from pages.image_to_text import show as image_to_text_show
    image_to_text_show()
