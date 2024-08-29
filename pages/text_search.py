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
        search_term = st.text_input("Enter the text to search for")
        if search_term:
            matches = [text for text in st.session_state['extracted_texts'] if search_term.lower() in text.lower()]
            st.write(f"Found {len(matches)} match(es):")
            for match in matches:
                # Display word count
                word_count = len(match.split())
                st.write(f"**Word Count:** {word_count}")

                # Highlight search term
                highlighted_text = highlight_search_term(match, search_term)
                st.markdown(highlighted_text, unsafe_allow_html=True)
        else:
            st.write("Please enter a search term.")
    else:
        st.error("⚠️ No text available to search. Please extract text first.")
