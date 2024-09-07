import streamlit as st
from fpdf import FPDF

def convert_txt_to_pdf(txt_file):
    """Convert TXT file to PDF."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in txt_file:
        pdf.multi_cell(0, 10, line)

    pdf_file_path = "output.pdf"
    pdf.output(pdf_file_path)
    return pdf_file_path

def show():
    st.title("📄 Convert TXT to PDF")

    uploaded_file = st.file_uploader("📂 Choose a TXT file", type=["txt"])

    if uploaded_file:
        if st.button("📝 Convert TXT to PDF"):
            try:
                # Read the uploaded TXT file
                txt_file = uploaded_file.read().decode("utf-8").splitlines()
                pdf_file_path = convert_txt_to_pdf(txt_file)
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