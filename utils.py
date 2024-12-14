import streamlit as st
import importlib
import json
import logging

# Load translations
with open('translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

def get_translation(text, language):
    """Get translation for the given text and language."""
    if language in translations and text in translations[language]:
        return translations[language][text]
    return text

def get_english_page_name(translated_name):
    """Get the English page name from the translated name."""
    for lang, trans in translations.items():
        for eng, tran in trans.items():
            if tran == translated_name:
                return eng
    return translated_name  # Return the original if no translation found

def setup_session_state():
    """Initialize session state variables."""
    if 'groq_api_key' not in st.session_state:
        st.session_state.groq_api_key = ""
    if 'extracted_texts' not in st.session_state:
        st.session_state.extracted_texts = []
    if 'language' not in st.session_state:
        st.session_state.language = "English"

def setup_logging():
    """Set up logging configuration for the application."""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )
    return logging.getLogger(__name__)

def load_page(page_name):
    """Load the specified page module."""
    try:
        # Get the English page name
        english_page_name = get_english_page_name(page_name)
        module_name = f"pages.{english_page_name.lower().replace(' ', '_')}"
        page_module = importlib.import_module(module_name)
        page_module.show()
    except ImportError as e:
        error_message = f"Error loading page {page_name}: {str(e)}"
        st.error(get_translation(error_message, st.session_state.language))
        log_error(error_message)

def handle_error(error_message):
    """Handle and display errors consistently."""
    translated_error = get_translation(f" An error occurred: {error_message}", st.session_state.language)
    st.error(translated_error)
    log_error(error_message)

def log_error(error_message):
    """Log errors to a file."""
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{error_message}\n")