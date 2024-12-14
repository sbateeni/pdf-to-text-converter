import re
import logging

logger = logging.getLogger(__name__)

def process_text(text, options=None):
    """
    Process the extracted text based on selected options.
    
    Args:
        text (str): The text to process
        options (dict): Dictionary of processing options
            - remove_extra_spaces (bool): Remove extra whitespace
            - remove_special_chars (bool): Remove special characters
            - lowercase (bool): Convert text to lowercase
    
    Returns:
        str: Processed text
    """
    if options is None:
        options = {}
    
    try:
        # Remove extra spaces if selected
        if options.get('remove_extra_spaces', False):
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
        
        # Remove special characters if selected
        if options.get('remove_special_chars', False):
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # Convert to lowercase if selected
        if options.get('lowercase', False):
            text = text.lower()
        
        return text
    
    except Exception as e:
        logger.error(f"Error processing text: {str(e)}")
        raise Exception(f"Failed to process text: {str(e)}")
