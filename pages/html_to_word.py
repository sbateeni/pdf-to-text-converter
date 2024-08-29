import os
import requests
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile
import pdfkit
import streamlit as st

def show():
    st.title(" Convert HTML to PDF")

    url = st.text_input("Enter the URL of the webpage", placeholder="https://example.com")

    def convert_url_to_pdf(url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Ensure correct encoding
            response.encoding = 'utf-8'
            html_content = response.text

            soup = BeautifulSoup(html_content, "html.parser")

            # Extract text and handle HTML entities
            text_content = soup.get_text(separator='\n', strip=True)

            # Create a temporary file to save the PDF document
            with NamedTemporaryFile(delete=False, suffix=".pdf", mode='wb') as temp_file:
                pdf_file_path = temp_file.name

            # Specify the path to the wkhtmltopdf executable
            wkhtmltopdf_path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

            # Save the text content to the PDF document
            pdfkit.from_string(text_content, pdf_file_path, configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path))

            return pdf_file_path

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while fetching the URL: {e}")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            return None

    if st.button("Convert URL to PDF"):
        if url:
            pdf_file_path = convert_url_to_pdf(url)
            if pdf_file_path:
                st.success("The webpage has been converted to a PDF document!")
                with open(pdf_file_path, "rb") as f:
                    st.download_button(
                        label="Download PDF File",
                        data=f,
                        file_name="converted_webpage.pdf"
                    )
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    show()