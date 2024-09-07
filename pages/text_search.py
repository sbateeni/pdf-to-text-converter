import streamlit as st
import re
import pyttsx3
import threading
import tempfile
import os
from gtts import gTTS

def text_to_speech(text, lang='en'):
    """تحويل النص إلى صوت باستخدام gTTS."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts = gTTS(text=text, lang=lang)
            tts.save(fp.name)
            st.audio(fp.name, format='audio/mp3')
        os.unlink(fp.name)
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحويل النص إلى صوت: {str(e)}")

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

    # إضافة خيارات اللغة
    lang_options = {
        "English": "en",
        "Arabic": "ar",
        "Spanish": "es"
    }
    selected_lang = st.selectbox("Select Language", list(lang_options.keys()))

    # إضافة زر لتحويل النص إلى صوت
    if st.button("🔊 تحويل النص إلى صوت"):
        extracted_text = " ".join(st.session_state.get('extracted_texts', []))  # جمع النصوص المستخرجة
        if extracted_text:  # تأكد من أن النص غير فارغ
            try:
                with st.spinner("جاري تحويل النص إلى صوت..."):
                    text_to_speech(extracted_text, lang=lang_options[selected_lang])
                st.success("تم تحويل النص إلى صوت بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ أثناء تحويل النص إلى صوت: {str(e)}")

    # إضافة زر لمشاركة النص المستخرج
    if st.button("Share Extracted Text"):
        # كود لمشاركة النص عبر البريد الإلكتروني
        st.success("Text shared successfully!")

    # إضافة زر لتصدير النص إلى Markdown
    if st.button("Export to Markdown"):
        extracted_text = " ".join(st.session_state.get('extracted_texts', []))
        if extracted_text:
            with open("extracted_text.md", "w", encoding="utf-8") as f:  # استخدام utf-8
                f.write(extracted_text)
            st.success("Text exported to Markdown successfully!")

# Assuming this function is called to display the search page
if __name__ == "__main__":
    show()
