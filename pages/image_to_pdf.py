import streamlit as st
import os
from tempfile import TemporaryDirectory
from fpdf import FPDF

def show():
    st.title("🖼️ Convert Images to PDF")

    uploaded_files = st.file_uploader("📂 Choose image files", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if st.button("💾 Convert to PDF"):
        if uploaded_files:
            with TemporaryDirectory() as temp_dir:
                images = []
                for uploaded_file in uploaded_files:
                    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(uploaded_file.read())
                    images.append(temp_file_path)

                pdf = FPDF()
                for image in images:
                    pdf.add_page()
                    pdf.image(image, x=10, y=10, w=190)

                pdf_file_path = os.path.join(temp_dir, "output.pdf")
                pdf.output(pdf_file_path)

                st.success("✅ Conversion completed!")
                with open(pdf_file_path, "rb") as f:
                    st.download_button(
                        label="📥 Download PDF File",
                        data=f,
                        file_name="output.pdf"
                    )
        else:
            st.error("⚠️ Please upload image files.")
