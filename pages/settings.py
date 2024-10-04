import streamlit as st
from utils import get_translation

def show():
    language = st.session_state.language
    st.title(get_translation("Settings", language))

    # Theme selection
    st.subheader(get_translation("Theme", language))
    theme = st.selectbox(
        get_translation("Select theme", language),
        ["Light", "Dark"],
        index=0 if st.session_state.get('theme', 'Light') == 'Light' else 1
    )
    st.session_state.theme = theme

    # Default language
    st.subheader(get_translation("Default Language", language))
    default_language = st.selectbox(
        get_translation("Select default language", language),
        ["English", "العربية", "Français", "Español", "中文"],
        index=["English", "العربية", "Français", "Español", "中文"].index(st.session_state.get('default_language', 'English'))
    )
    st.session_state.default_language = default_language

    # Google AI API Key
    st.subheader(get_translation("Google AI API Key", language))
    google_ai_api_key = st.text_input(
        get_translation("Enter Google AI API Key", language),
        value=st.session_state.get("google_ai_api_key", ""),
        type="password"
    )
    if google_ai_api_key:
        st.session_state.google_ai_api_key = google_ai_api_key

    # Save settings
    if st.button(get_translation("Save Settings", language)):
        st.success(get_translation("Settings saved successfully!", language))

if __name__ == "__main__":
    show()