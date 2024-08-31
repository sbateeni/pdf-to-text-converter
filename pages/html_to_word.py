import requests
from bs4 import BeautifulSoup
import streamlit as st
import re
from langdetect import detect

def show():
    st.title("Fetch URL Content")

    url = st.text_input("Enter the URL of the webpage", placeholder="https://example.com")

    # Add language selection option
    languages = ["Auto-detect", "English", "Arabic", "French", "Spanish", "German"]
    selected_language = st.selectbox("Select Language", languages)

    def clean_text(text):
        # Remove control characters and NULL bytes
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)
        # Replace non-breaking spaces with regular spaces
        text = text.replace('\xa0', ' ')
        # Remove any HTML tags that might have been left
        text = re.sub(r'<[^>]+>', '', text)
        return text

    def detect_language(text):
        try:
            return detect(text)
        except:
            return "unknown"

    def fetch_url_content(url, selected_language):
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Ensure correct encoding
            response.encoding = 'utf-8'
            html_content = response.text

            soup = BeautifulSoup(html_content, "html.parser")

            # Extract text and handle HTML entities
            text_content = soup.get_text(separator='\n', strip=True)

            # Clean the text content
            cleaned_text = clean_text(text_content)

            # Detect or use selected language
            if selected_language == "Auto-detect":
                language = detect_language(cleaned_text)
            else:
                language = selected_language

            return cleaned_text, language

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while fetching the URL: {e}")
            return None, None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return None, None

    if st.button("Fetch URL Content"):
        if url:
            content, detected_language = fetch_url_content(url, selected_language)
            if content:
                st.success(f"The webpage content has been fetched! Language: {detected_language}")
                st.subheader("Full Content:")
                st.text_area("Fetched Content", content, height=300)
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    show()