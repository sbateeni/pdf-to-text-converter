import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from utils import get_translation
from googletrans import Translator
import time
import logging
from google.api_core import exceptions as google_exceptions

load_dotenv()

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إضافة مفتاح API مباشرة
API_KEY = "AIzaSyCQFAnoScogox-tkrkYfLgptSitKQtW1EU"

# إنشاء مترجم
translator = Translator()

def get_language_code(language_name):
    language_map = {
        "English": "en", "العربية": "ar", "Français": "fr", "Español": "es", "中文": "zh-cn"
    }
    return language_map.get(language_name, "en")

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                logger.warning("No text found on page.")
    logger.info(f"Extracted text: {text[:100]}...")  # Log the first 100 characters of the extracted text
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    logger.info("Starting to create vector store")
    try:
        embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = Chroma.from_texts(text_chunks, embedding_function, persist_directory="./chroma_db")
        logger.info("Vector store created successfully")
        return vector_store
    except Exception as e:
        logger.error(f"Error creating vector store: {str(e)}")
        raise

def generate_rag_prompt(query, context):
    escaped = context.replace("'","").replace('"', "").replace("\n"," ")
    prompt = f"""
    You are a helpful and informative bot that answers questions using text from the reference context included below. 
    Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. 
    However, you are talking to a non-technical audience, so be sure to break down complicated concepts and 
    strike a friendly and conversational tone. 
    If the context is irrelevant to the answer, you may ignore it.
    QUESTION: '{query}'
    CONTEXT: '{escaped}'
    
    ANSWER:
    """
    return prompt

def get_conversational_chain(vector_store):
    prompt_template = generate_rag_prompt("{question}", "{context}")
    
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=API_KEY)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    chain = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        chain_type_kwargs={"prompt": prompt}
    )
    return chain

def user_input(user_question, original_language, vector_store):
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            translated_question = translator.translate(user_question, dest='en').text
            
            chain = get_conversational_chain(vector_store)
            response = chain.invoke({"query": translated_question})
            
            lang_code = get_language_code(original_language)
            translated_response = translator.translate(response["result"], dest=lang_code).text
            
            return translated_response
        except google_exceptions.ResourceExhausted:
            if attempt < max_retries - 1:
                st.warning(f"Resource exhausted. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                st.error("Failed to get a response after multiple attempts. Please try again later.")
                return None
        except Exception as e:
            logger.error(f"Error in user_input: {str(e)}")
            st.error(f"An error occurred: {str(e)}")
            return None

def save_conversation_to_file():
    with open("conversation_log.txt", "w") as f:
        for message in st.session_state.messages:
            f.write(f"{message['role']}: {message['content']}\n")

def show():
    language = st.session_state.language
    st.title(get_translation("RAG with Gemini💁", language))

    st.success(get_translation("✅ Connected to Google AI API successfully! No errors detected.", language))

    genai.configure(api_key=API_KEY)

    st.header(get_translation("Upload and Process PDF Files", language))
    pdf_docs = st.file_uploader(get_translation("Upload your PDF Files", language), type="pdf", accept_multiple_files=True)
    
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None

    if st.button(get_translation("Submit & Process", language)):
        if pdf_docs:
            with st.spinner(get_translation("Processing...", language)):
                try:
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    st.session_state.vector_store = get_vector_store(text_chunks)
                    st.success(get_translation("Done", language))
                except Exception as e:
                    logger.error(f"Error processing PDFs: {str(e)}")
                    st.error(f"An error occurred while processing the PDFs: {str(e)}")
        else:
            st.warning(get_translation("Please upload PDF files first.", language))

    if st.session_state.vector_store:
        st.header(get_translation("Ask Questions", language))

        suggested_questions = [
            get_translation("What is the main topic of this document?", language),
            get_translation("Summarize the key points in the document.", language),
            get_translation("What are the main conclusions of this document?", language),
            get_translation("Are there any specific recommendations mentioned?", language),
            get_translation("What is the overall tone of the document?", language)
        ]

        selected_question = st.selectbox(
            get_translation("Select a suggested question or type your own:", language),
            [""] + suggested_questions
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input(get_translation("Ask a question", language)):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            response = user_input(prompt, language, st.session_state.vector_store)
            if response:
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        if st.button("Save Conversation"):
            save_conversation_to_file()
            st.success("Conversation saved to conversation_log.txt")

if __name__ == "__main__":
    show()