from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import fonts
from reportlab.lib.fonts import tt2ps


def save_text_to_pdf(extracted_texts, uploaded_filename):
    pdf_file_path = uploaded_filename.replace(".pdf", "_converted.pdf")

    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter

    for text in extracted_texts:
        c.setFont("Helvetica", 12)
        text_object = c.beginText(40, height - 40)
        text_object.setTextOrigin(40, height - 40)
        text_object.textLines(text)
        c.drawText(text_object)
        c.showPage()

    c.save()

    return pdf_file_path
