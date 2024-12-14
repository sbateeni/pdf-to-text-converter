import os
import pytesseract
import logging

logger = logging.getLogger(__name__)

def setup_tesseract(languages=['eng', 'ara', 'spa']):
    """
    Set up Tesseract OCR with specified languages.
    On Streamlit Cloud, Tesseract and language packs are installed via packages.txt
    """
    try:
        # Test if Tesseract is available
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
        
        # Test if languages are available
        installed_langs = pytesseract.get_languages()
        logger.info(f"Installed languages: {installed_langs}")
        
        # Check if all required languages are available
        missing_langs = [lang for lang in languages if lang not in installed_langs]
        if missing_langs:
            logger.warning(f"Missing language packs: {missing_langs}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Error setting up Tesseract: {str(e)}")
        return False

def perform_ocr(image, lang='eng'):
    """
    Perform OCR on an image using Tesseract.
    """
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        logger.error(f"Error performing OCR: {str(e)}")
        raise Exception(f"OCR failed: {str(e)}")
