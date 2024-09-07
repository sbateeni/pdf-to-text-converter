import streamlit as st

def show():
    st.title("⚙️ Settings")

    # اختيار اللغة الافتراضية
    default_language = st.selectbox("Select Default Language", ["English", "Arabic", "Spanish"])

    # إعدادات الصوت
    speech_speed = st.slider("Set Speech Speed", min_value=100, max_value=300, value=150)

    st.write("Settings saved successfully!")

if __name__ == "__main__":
    show()