import streamlit as st
from docx2pdf import convert
import os
import tempfile

def show():
    st.title("📄 Convert Word to PDF")

    # Create a file uploader for Word files
    uploaded_file = st.file_uploader("📂 Choose a Word file or drag and drop here", type=["docx"])

    if uploaded_file:
        # Show the name of the uploaded file
        st.write(f"File Uploaded: {uploaded_file.name}")

        if st.button("📝 Convert Word to PDF"):
            try:
                # Create a temporary file to save the uploaded .docx file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_word:
                    temp_word.write(uploaded_file.getvalue())
                    temp_word_path = temp_word.name

                # Set output PDF file path
                output_pdf_path = temp_word_path.replace(".docx", ".pdf")

                # Convert Word to PDF
                convert(temp_word_path, output_pdf_path)

                st.success("✅ Conversion completed!")
                
                # Provide a download link for the PDF file
                with open(output_pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF Document",
                        data=pdf_file.read(),
                        file_name=uploaded_file.name.replace('.docx', '.pdf'),
                        mime="application/pdf"
                    )
                
                # Clean up the temporary files
                os.unlink(temp_word_path)
                os.unlink(output_pdf_path)
            except Exception as e:
                st.error(f"❌ An error occurred during conversion: {str(e)}")

if __name__ == "__main__":
    show()