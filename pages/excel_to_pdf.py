import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile

def convert_excel_to_pdf(excel_file):
    """Convert Excel file to PDF."""
    df = pd.read_excel(excel_file)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    col_width = pdf.w / len(df.columns)
    row_height = pdf.font_size * 1.5
    
    for header in df.columns:
        pdf.cell(col_width, row_height, str(header), border=1)
    pdf.ln(row_height)
    
    for row in df.itertuples(index=False):
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln(row_height)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        pdf_file_path = temp_file.name
        pdf.output(pdf_file_path)
    
    return pdf_file_path

def show():
    st.title("📄 Convert Excel to PDF")

    uploaded_file = st.file_uploader("📂 Choose an Excel file", type=["xlsx"])

    if uploaded_file:
        if st.button("📝 Convert Excel to PDF"):
            try:
                pdf_file_path = convert_excel_to_pdf(uploaded_file)
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