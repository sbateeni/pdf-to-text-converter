import streamlit as st
from utils import handle_error, get_translation
from PyPDF2 import PdfReader, PdfWriter
import io
import requests

def extract_text_from_pdf(pdf_file):
    """استخراج النص من ملف PDF."""
    pdf_reader = PdfReader(pdf_file)
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text() or ""  # تأكد من التعامل مع الصفحات الفارغة
    return pdf_text

def send_rag_query(api_key, pdf_text):
    """إرسال استعلام RAG إلى Groq API باستخدام GraphQL."""
    endpoint = "https://api.groq.com/v1/graphql"  # تأكد من استخدام المسار الصحيح
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # تعريف استعلام GraphQL
    query = """
        mutation ($query: String!, $context: String!, $model: String!, $maxTokens: Int!, $temperature: Float!, $topP: Float!) {
            generateText(input: {
                query: $query,
                context: $context,
                model: $model,
                maxTokens: $maxTokens,
                temperature: $temperature,
                topP: $topP
            }) {
                text
            }
        }
    """
    
    # تعريف متغيرات الاستعلام
    variables = {
        "query": "Summarize the main points of this text.",
        "context": pdf_text,
        "model": "rag",
        "maxTokens": 256,
        "temperature": 0.7,
        "topP": 0.9
    }
    
    # إرسال الاستعلام إلى API
    response = requests.post(
        endpoint,
        headers=headers,
        json={"query": query, "variables": variables}
    )
    
    if response.status_code == 200:
        return response.json()  # إرجاع الاستجابة بتنسيق JSON
    else:
        st.error(f"❌ {get_translation('Error sending RAG query', st.session_state.language)}: {response.text}")
        return None

def merge_pdfs(pdf_files):
    pdf_writer = PdfWriter()
    for pdf_file in pdf_files:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    
    output = io.BytesIO()
    pdf_writer.write(output)
    output.seek(0)
    return output

def show():
    language = st.session_state.language
    st.title(get_translation("GROQ PDF Merge", language))

    api_key = st.text_input(get_translation("Enter GROQ API Key", language), value=st.session_state.get("groq_api_key", ""), type="password")
    
    if api_key:
        st.session_state.groq_api_key = api_key
        st.success(get_translation("✅ API connected successfully!", language))
    elif "groq_api_key" in st.session_state:
        st.info(get_translation("ℹ️ API key already stored", language))

    uploaded_files = st.file_uploader(get_translation("Upload PDF files", language), type="pdf", accept_multiple_files=True)

    if uploaded_files and st.button(get_translation("Merge and Process PDFs", language)):
        try:
            merged_pdf = merge_pdfs(uploaded_files)
            st.download_button(
                label=get_translation("Download Merged PDF", language),
                data=merged_pdf,
                file_name="merged.pdf",
                mime="application/pdf"
            )

            pdf_text = extract_text_from_pdf(merged_pdf)
            rag_response = send_rag_query(api_key, pdf_text)

            if rag_response:
                st.subheader(get_translation("GROQ API Response", language))
                st.json(rag_response)
        except Exception as e:
            handle_error(str(e))

if __name__ == "__main__":
    show()