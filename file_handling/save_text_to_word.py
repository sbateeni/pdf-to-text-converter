from docx import Document
import os

def save_text_to_word(texts, pdf_filename):
    # Determine the output directory relative to the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the path for the Word file
    base_name = os.path.splitext(pdf_filename)[0]
    word_file_path = os.path.join(output_dir, f"{base_name}.docx")

    # Create a new Word document
    doc = Document()
    for i, text in enumerate(texts):
        doc.add_heading(f'Page {i + 1}', level=1)
        doc.add_paragraph(text)

    # Save the document to the specified path
    doc.save(word_file_path)

    return word_file_path
