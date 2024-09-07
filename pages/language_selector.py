import streamlit as st

def show():
    st.title("🌐 Language Selector")

    # إضافة خيارات للغات متعددة
    languages = ["English", "Arabic", "Spanish", "French"]
    selected_language = st.selectbox("Select Language", languages)

    if selected_language == "Arabic":
        st.write("مرحبا بكم في تطبيق تحويل PDF!")
    else:
        st.write("Welcome to the PDF Converter App!")

if __name__ == "__main__":
    show()