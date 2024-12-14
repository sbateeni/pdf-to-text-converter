import streamlit as st
import logging
from textblob import TextBlob
from collections import Counter
import re
import arabic_reshaper
from bidi.algorithm import get_display

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Text Analysis", page_icon="📊", layout="wide")

def analyze_text(text, lang):
    """Analyze text and return statistics"""
    try:
        # Basic statistics
        words = text.split()
        sentences = text.split('.')
        chars = len(text)
        
        # Word frequency
        word_freq = Counter(words)
        most_common = word_freq.most_common(10)
        
        # Sentiment analysis (for English and Spanish)
        sentiment = None
        if lang in ['eng', 'spa']:
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'char_count': chars,
            'most_common': most_common,
            'sentiment': sentiment
        }
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        raise

def main():
    st.title("Text Analysis")
    st.write("Analyze your text and get insights")

    # Text input
    input_text = st.text_area("Enter or paste your text here", height=200)
    
    if input_text:
        # Language selection
        lang = st.selectbox(
            "Select text language",
            options=['eng', 'ara', 'spa'],
            format_func=lambda x: {'eng': 'English', 'ara': 'Arabic', 'spa': 'Spanish'}[x]
        )

        if st.button("Analyze Text"):
            try:
                # Process Arabic text if needed
                display_text = input_text
                if lang == 'ara':
                    display_text = get_display(arabic_reshaper.reshape(input_text))

                # Get analysis results
                results = analyze_text(input_text, lang)

                # Display results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Word Count", results['word_count'])
                
                with col2:
                    st.metric("Sentence Count", results['sentence_count'])
                
                with col3:
                    st.metric("Character Count", results['char_count'])

                # Word frequency
                st.subheader("Most Common Words")
                freq_df = pd.DataFrame(results['most_common'], 
                                     columns=['Word', 'Frequency'])
                st.bar_chart(freq_df.set_index('Word'))

                # Sentiment analysis (for supported languages)
                if results['sentiment'] is not None:
                    st.subheader("Sentiment Analysis")
                    sentiment = results['sentiment']
                    if sentiment > 0:
                        st.success(f"Positive sentiment (Score: {sentiment:.2f})")
                    elif sentiment < 0:
                        st.error(f"Negative sentiment (Score: {sentiment:.2f})")
                    else:
                        st.info(f"Neutral sentiment (Score: {sentiment:.2f})")

            except Exception as e:
                st.error(f"Error analyzing text: {str(e)}")
                logger.error(f"Error analyzing text: {str(e)}")

if __name__ == "__main__":
    main()
