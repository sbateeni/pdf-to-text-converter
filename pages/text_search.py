import streamlit as st
import re


def highlight_search_term(text, search_term):
    """Highlight the search term in the text."""
    highlighted_text = re.sub(f"({re.escape(search_term)})", r"<mark>\1</mark>", text, flags=re.IGNORECASE)
    return highlighted_text


def show():
    st.title("🔍 Search Text")

    # Initialize session state for extracted_texts
    if 'extracted_texts' not in st.session_state:
        st.session_state['extracted_texts'] = []

    if st.session_state['extracted_texts']:
        # Add button to show extracted text
        if st.button("Show Extracted Text", key="show_extracted_text_button_search"):
            for text in st.session_state['extracted_texts']:
                st.write(text)
    else:
        st.error("⚠️ No text available to search. Please extract text first.")

    # Add search functionality
    search_term = st.text_input("Enter search term:")
    if search_term:
        for i, text in enumerate(st.session_state['extracted_texts']):
            if search_term.lower() in text.lower():
                st.subheader(f"Match found in text {i+1}:")
                highlighted_text = highlight_search_term(text, search_term)
                st.markdown(highlighted_text, unsafe_allow_html=True)


# Assuming this function is called to display the search page
if __name__ == "__main__":
    show()
