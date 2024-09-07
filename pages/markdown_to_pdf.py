import streamlit as st
import markdown
from weasyprint import HTML

def show():
    st.title("📄 Convert Markdown to PDF")

    markdown_text = st.text_area("Enter Markdown content here:")

    if st.button("Convert to PDF"):
        try:
            html_content = markdown.markdown(markdown_text)
            pdf_file_path = "output.pdf"
            HTML(string=html_content).write_pdf(pdf_file_path)
            st.success("✅ Conversion completed!")

            with open(pdf_file_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download PDF Document",
                    data=pdf_file.read(),
                    file_name="output.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"❌ An error occurred during conversion: {str(e)}")

if __name__ == "__main__":
    show()