import streamlit as st
import pypandoc

def convert_rtf_to_pdf(rtf_file):
    """Convert RTF file to PDF."""
    pdf_file_path = "output.pdf"
    pypandoc.convert_file(rtf_file, 'pdf', outputfile=pdf_file_path)
    return pdf_file_path

def show():
    st.title("📄 Convert RTF to PDF")

    uploaded_file = st.file_uploader("📂 Choose an RTF file", type=["rtf"])

    if uploaded_file:
        if st.button("📝 Convert RTF to PDF"):
            try:
                pdf_file_path = convert_rtf_to_pdf(uploaded_file)
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