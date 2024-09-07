import streamlit as st

# Streamlit app setup
st.title("📄✨ PDF Converter and Text Extractor")
st.markdown("Convert PDF files to images, extract text, and convert to Word.")

# Sidebar for navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Text Search", "Image Viewer", "HTML to Word", "Image to PDF", "Convert Image to Text", "Word to PDF", "Excel to PDF", "CSV to Excel", "JSON to CSV", "XML to JSON", "TXT to PDF", "PPTX to PDF", "PDF to Images", "HTML to Markdown", "YAML to JSON", "RTF to PDF", "Settings", "About", "Help", "Error Log", "Language Selector"])

# Load the corresponding page based on the selection
if page == "Home":
    from pages.home import show as home_show
    home_show()

elif page == "Text Search":
    from pages.text_search import show as text_search_show
    text_search_show()

elif page == "Image Viewer":
    from pages.image_viewer import show as image_viewer_show
    image_viewer_show()

elif page == "HTML to Word":
    from pages.html_to_word import show as html_to_word_show
    html_to_word_show()

elif page == "Image to PDF":
    from pages.image_to_pdf import show as image_to_pdf_show
    image_to_pdf_show()

elif page == "Convert Image to Text":
    from pages.image_to_text import show as image_to_text_show
    image_to_text_show()

elif page == "Word to PDF":
    from pages.word_to_pdf import show as word_to_pdf_show
    word_to_pdf_show()

elif page == "Excel to PDF":
    from pages.excel_to_pdf import show as excel_to_pdf_show
    excel_to_pdf_show()

elif page == "CSV to Excel":
    from pages.csv_to_excel import show as csv_to_excel_show
    csv_to_excel_show()

elif page == "JSON to CSV":
    from pages.json_to_csv import show as json_to_csv_show
    json_to_csv_show()

elif page == "XML to JSON":
    from pages.xml_to_json import show as xml_to_json_show
    xml_to_json_show()

elif page == "TXT to PDF":
    from pages.txt_to_pdf import show as txt_to_pdf_show
    txt_to_pdf_show()

elif page == "PPTX to PDF":
    from pages.pptx_to_pdf import show as pptx_to_pdf_show
    pptx_to_pdf_show()

elif page == "PDF to Images":
    from pages.pdf_to_image import show as pdf_to_image_show
    pdf_to_image_show()

elif page == "HTML to Markdown":
    from pages.html_to_markdown import show as html_to_markdown_show
    html_to_markdown_show()

elif page == "YAML to JSON":
    from pages.yaml_to_json import show as yaml_to_json_show
    yaml_to_json_show()

elif page == "RTF to PDF":
    from pages.rtf_to_pdf import show as rtf_to_pdf_show
    rtf_to_pdf_show()

elif page == "Settings":
    from pages.settings import show as settings_show
    settings_show()

elif page == "About":
    from pages.about import show as about_show
    about_show()

elif page == "Help":
    from pages.help import show as help_show
    help_show()

elif page == "Error Log":
    from pages.error_log import show as error_log_show
    error_log_show()

elif page == "Language Selector":
    from pages.language_selector import show as language_selector_show
    language_selector_show()
