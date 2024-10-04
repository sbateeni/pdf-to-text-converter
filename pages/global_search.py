import streamlit as st
from utils import get_translation

def show():
    language = st.session_state.language
    st.title(get_translation("Global Search", language))

    search_query = st.text_input(get_translation("Enter search query", language))

    if search_query:
        st.subheader(get_translation("Search Results", language))
        # Here you would implement the actual search functionality
        # For now, we'll just display a placeholder message
        st.write(get_translation("Searching for:", language), search_query)
        st.info(get_translation("Search functionality to be implemented", language))

if __name__ == "__main__":
    show()