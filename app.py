import streamlit as st
from utils import load_page, setup_session_state, get_translation, get_english_page_name

# Streamlit app setup
st.set_page_config(page_title="PDF Converter and Text Extractor", page_icon="📄✨")

# Setup session state
setup_session_state()

# Language selector
languages = ["English", "العربية", "Français", "Español", "中文"]
selected_language = st.sidebar.selectbox("🌐 Select Language", languages)
st.session_state.language = selected_language

# Translate title and description
title = get_translation("PDF Converter and Text Extractor", selected_language)
description = get_translation("Convert PDF files to images, extract text, and convert to various formats.", selected_language)

st.title(f"📄✨ {title}")
st.markdown(description)

# Sidebar for navigation
st.sidebar.title(get_translation("🔍 Navigation", selected_language))
page_options = [
    "Home", 
    "GROQ PDF Merge",
    "RAG with Gemini",  # إضافة الصفحة الجديدة هنا
    "Text Search", 
    "Image Viewer", 
    "HTML to Word", 
    "Image to PDF", 
    "Convert Image to Text", 
    "Word to PDF", 
    "Excel to PDF", 
    "CSV to Excel", 
    "JSON to CSV", 
    "XML to JSON", 
    "TXT to PDF", 
    "PPTX to PDF", 
    "PDF to Images", 
    "HTML to Markdown", 
    "YAML to JSON", 
    "RTF to PDF", 
    "Settings", 
    "About", 
    "Help", 
    "Error Log"
]

page = st.sidebar.radio(get_translation("Go to", selected_language), 
                        [get_translation(option, selected_language) for option in page_options])

# Add a progress bar to the main page
progress_bar = st.progress(0)

# Add a status message to the main page
status_message = st.empty()

# Update progress and status
def update_progress(progress, message):
    progress_bar.progress(progress)
    status_message.text(message)

# Load the corresponding page based on the selection
update_progress(50, get_translation("Loading page...", selected_language))
load_page(page)
update_progress(100, get_translation("Page loaded successfully!", selected_language))

# Clear the progress bar and status message after a short delay
import time
time.sleep(1)  # Wait for 1 second
progress_bar.empty()
status_message.empty()
