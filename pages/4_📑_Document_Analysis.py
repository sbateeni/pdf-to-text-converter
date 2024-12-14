import streamlit as st
import tempfile
from pathlib import Path
import logging
from PyPDF2 import PdfReader
from textblob import TextBlob
import pandas as pd
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Document Analysis", page_icon="📑", layout="wide")

def extract_structure(pdf_path):
    """Extract document structure including headers, paragraphs, and lists"""
    try:
        reader = PdfReader(pdf_path)
        structure = []
        
        for page in reader.pages:
            text = page.extract_text()
            
            # Split into lines
            lines = text.split('\n')
            
            current_section = {'type': 'text', 'content': []}
            
            for line in lines:
                # Detect headers (lines with less than 5 words and ending with numbers or all caps)
                if len(line.split()) < 5 and (line.strip().isupper() or re.search(r'\d+$', line)):
                    if current_section['content']:
                        structure.append(current_section)
                        current_section = {'type': 'text', 'content': []}
                    structure.append({'type': 'header', 'content': line.strip()})
                
                # Detect lists (lines starting with bullets or numbers)
                elif re.match(r'^[\d•\-\*]\s+', line):
                    if current_section['type'] != 'list':
                        if current_section['content']:
                            structure.append(current_section)
                        current_section = {'type': 'list', 'content': []}
                    current_section['content'].append(line.strip())
                
                # Regular paragraph text
                else:
                    if current_section['type'] == 'list' and current_section['content']:
                        structure.append(current_section)
                        current_section = {'type': 'text', 'content': []}
                    current_section['content'].append(line.strip())
        
        if current_section['content']:
            structure.append(current_section)
        
        return structure
    except Exception as e:
        logger.error(f"Error extracting document structure: {str(e)}")
        raise

def extract_tables(pdf_path):
    """Extract tables from PDF using tabula"""
    try:
        import tabula
        tables = tabula.read_pdf(pdf_path, pages='all')
        return tables
    except Exception as e:
        logger.error(f"Error extracting tables: {str(e)}")
        return []

def analyze_keywords(text):
    """Extract and analyze keywords using TF-IDF"""
    try:
        # Tokenize and clean text
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Remove common stop words
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        words = [w for w in words if w not in stop_words]
        
        # Calculate word frequencies
        word_freq = Counter(words)
        
        # Use TF-IDF for keyword extraction
        vectorizer = TfidfVectorizer(max_features=20)
        tfidf = vectorizer.fit_transform([text])
        
        # Get feature names and scores
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf.toarray()[0]
        
        # Create keyword dictionary with scores
        keywords = dict(zip(feature_names, scores))
        return {k: v for k, v in sorted(keywords.items(), key=lambda x: x[1], reverse=True)}
    except Exception as e:
        logger.error(f"Error analyzing keywords: {str(e)}")
        return {}

def analyze_readability(text):
    """Analyze text readability using various metrics"""
    try:
        # Basic statistics
        words = text.split()
        sentences = text.split('.')
        syllables = sum([len(re.findall(r'[aeiou]+', word.lower())) for word in words])
        
        # Calculate metrics
        avg_word_length = sum(len(word) for word in words) / len(words)
        avg_sentence_length = len(words) / len(sentences)
        
        # Flesch Reading Ease
        flesch = 206.835 - 1.015 * avg_sentence_length - 84.6 * (syllables / len(words))
        
        return {
            'total_words': len(words),
            'total_sentences': len(sentences),
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'flesch_score': round(flesch, 2)
        }
    except Exception as e:
        logger.error(f"Error analyzing readability: {str(e)}")
        return {}

def main():
    st.title("Document Analysis")
    st.write("Analyze your document's structure, content, and readability")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "temp.pdf"
            pdf_path.write_bytes(uploaded_file.getvalue())
            
            # Create tabs for different analyses
            tabs = st.tabs(["Document Structure", "Content Analysis", "Readability Metrics"])
            
            try:
                # Extract text from PDF
                reader = PdfReader(str(pdf_path))
                full_text = ""
                for page in reader.pages:
                    full_text += page.extract_text() + "\n"
                
                # Tab 1: Document Structure
                with tabs[0]:
                    st.subheader("Document Structure")
                    structure = extract_structure(str(pdf_path))
                    
                    for item in structure:
                        if item['type'] == 'header':
                            st.markdown(f"### {item['content']}")
                        elif item['type'] == 'list':
                            for line in item['content']:
                                st.markdown(f"- {line}")
                        else:
                            st.write(' '.join(item['content']))
                    
                    # Extract and display tables
                    tables = extract_tables(str(pdf_path))
                    if tables:
                        st.subheader("Tables Found")
                        for i, table in enumerate(tables):
                            st.write(f"Table {i+1}")
                            st.dataframe(table)
                
                # Tab 2: Content Analysis
                with tabs[1]:
                    st.subheader("Keyword Analysis")
                    keywords = analyze_keywords(full_text)
                    
                    # Create keyword visualization
                    fig = go.Figure(data=[go.Bar(
                        x=list(keywords.keys()),
                        y=list(keywords.values()),
                        text=list(keywords.values()),
                        textposition='auto',
                    )])
                    fig.update_layout(
                        title="Top Keywords (TF-IDF Score)",
                        xaxis_title="Keywords",
                        yaxis_title="TF-IDF Score"
                    )
                    st.plotly_chart(fig)
                    
                    # Word frequency analysis
                    words = re.findall(r'\b\w+\b', full_text.lower())
                    word_freq = Counter(words).most_common(20)
                    
                    freq_df = pd.DataFrame(word_freq, columns=['Word', 'Frequency'])
                    st.subheader("Word Frequency")
                    st.bar_chart(freq_df.set_index('Word'))
                
                # Tab 3: Readability Metrics
                with tabs[2]:
                    st.subheader("Readability Analysis")
                    metrics = analyze_readability(full_text)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Words", metrics['total_words'])
                        st.metric("Average Word Length", f"{metrics['avg_word_length']} characters")
                    
                    with col2:
                        st.metric("Total Sentences", metrics['total_sentences'])
                        st.metric("Average Sentence Length", f"{metrics['avg_sentence_length']} words")
                    
                    with col3:
                        flesch_score = metrics['flesch_score']
                        st.metric("Flesch Reading Ease", flesch_score)
                        
                        # Interpret Flesch score
                        if flesch_score >= 90:
                            st.success("Very Easy to Read")
                        elif flesch_score >= 80:
                            st.success("Easy to Read")
                        elif flesch_score >= 70:
                            st.info("Fairly Easy to Read")
                        elif flesch_score >= 60:
                            st.info("Standard")
                        elif flesch_score >= 50:
                            st.warning("Fairly Difficult")
                        else:
                            st.error("Difficult to Read")
                
            except Exception as e:
                st.error(f"Error analyzing document: {str(e)}")
                logger.error(f"Error analyzing document: {str(e)}")

if __name__ == "__main__":
    main()
