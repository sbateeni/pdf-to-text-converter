import streamlit as st
import logging
from textblob import TextBlob
import arabic_reshaper
from bidi.algorithm import get_display

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Text Editor", page_icon="📝", layout="wide")

def process_text(text, lang, options):
    """Process text with selected options"""
    try:
        if options.get('remove_extra_spaces'):
            text = " ".join(text.split())
        
        if options.get('remove_special_chars'):
            text = ''.join(c for c in text if c.isalnum() or c.isspace())
        
        if options.get('make_lowercase'):
            text = text.lower()
            
        if options.get('correct_spelling'):
            if lang == 'ara':
                text = arabic_reshaper.reshape(text)
                text = get_display(text)
            else:
                blob = TextBlob(text)
                text = str(blob.correct())
                
        return text
    except Exception as e:
        logger.error(f"Error processing text: {str(e)}")
        raise

def main():
    st.title("Text Editor")
    st.write("Edit and process extracted text")

    # Text input
    input_text = st.text_area("Enter or paste your text here", height=200)
    
    if input_text:
        # Language selection
        lang = st.selectbox(
            "Select text language",
            options=['eng', 'ara', 'spa'],
            format_func=lambda x: {'eng': 'English', 'ara': 'Arabic', 'spa': 'Spanish'}[x]
        )

        # Processing options
        st.subheader("Text Processing Options")
        col1, col2 = st.columns(2)
        
        with col1:
            remove_spaces = st.checkbox("Remove Extra Spaces")
            remove_special = st.checkbox("Remove Special Characters")
        
        with col2:
            make_lowercase = st.checkbox("Convert to Lowercase")
            correct_spelling = st.checkbox("Correct Spelling")

        if st.button("Process Text"):
            try:
                processed_text = process_text(input_text, lang, {
                    'remove_extra_spaces': remove_spaces,
                    'remove_special_chars': remove_special,
                    'make_lowercase': make_lowercase,
                    'correct_spelling': correct_spelling
                })

                st.subheader("Processed Text")
                st.text_area("", processed_text, height=200)

                # Download button
                st.download_button(
                    label="Download Processed Text",
                    data=processed_text,
                    file_name="processed_text.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error processing text: {str(e)}")
                logger.error(f"Error processing text: {str(e)}")

if __name__ == "__main__":
    main()
