import streamlit as st
from PIL import Image
import pytesseract

def show():
    st.title("🖼️ Convert Image to Text")

    # Create a file uploader for images
    uploaded_file = st.file_uploader("📂 Choose an image file", type=["jpg", "jpeg", "png"])

    # Add language selection option
    languages = ["Automatic", "English", "Arabic", "Spanish", "French", "German"]  # إضافة لغات جديدة
    selected_language = st.selectbox("🌐 Select Language", languages)

    # Define language codes
    lang_code = {
        'English': 'eng',
        'Arabic': 'ara',
        'Spanish': 'spa'
    }

    # Set default languages for 'Automatic'
    if selected_language == 'Automatic':
        lang_codes = ['eng', 'ara']  # Default to English and Arabic
    else:
        lang_codes = [lang_code.get(selected_language, '')]

    # Join lang_codes into a comma-separated string for pytesseract
    lang_codes_str = '+'.join(lang_codes)

    def extract_text_from_image(image):
        return pytesseract.image_to_string(image, lang=lang_codes_str)

    if st.button("🔍 Extract Text"):
        if uploaded_file:
            try:
                # Open the image file
                image = Image.open(uploaded_file)
                # Extract text from the image
                extracted_text = extract_text_from_image(image)

                st.success("✅ Text extraction completed!")
                st.text_area("Extracted Text", extracted_text, height=300)
            except Exception as e:
                st.error(f"❌ An error occurred during extraction: {str(e)}")
                # تسجيل الخطأ في ملف
                with open("error_log.txt", "a") as log_file:
                    log_file.write(f"{str(e)}\n")
        else:
            st.warning("⚠️ Please upload an image file.")

if __name__ == "__main__":
    show()