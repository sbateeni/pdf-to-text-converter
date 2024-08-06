from fpdf import FPDF
import os


def save_text_to_pdf(texts, pdf_filename):
    # Determine the output directory relative to the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the path for the PDF file
    base_name = os.path.splitext(pdf_filename)[0]
    pdf_file_path = os.path.join(output_dir, f"{base_name}.pdf")

    # Create a new PDF document
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for i, text in enumerate(texts):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)

    # Save the document to the specified path
    pdf.output(pdf_file_path)
    return pdf_file_path
