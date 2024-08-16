# file_handling/save_text_to_word.py

from docx import Document


def save_text_to_word(extracted_texts, uploaded_filename, search_query=""):
    doc = Document()
    for i, text in enumerate(extracted_texts):
        doc.add_heading(f'Page {i + 1}', level=1)
        if search_query:
            # Highlight search_query in the text
            highlighted_text = text.replace(search_query, f'**{search_query}**')
            doc.add_paragraph(highlighted_text)
        else:
            doc.add_paragraph(text)

    # Save the Word document
    word_filename = uploaded_filename.replace(".pdf", ".docx")
    word_file_path = f"temp_{word_filename}"
    doc.save(word_file_path)

    return word_file_path
