import logging
from pathlib import Path
import pytesseract
from PIL import Image, ImageEnhance
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from textblob import TextBlob
import arabic_reshaper
from bidi.algorithm import get_display
from langdetect import detect, DetectorFactory
import numpy as np
import cv2
from deskew import determine_skew
from skimage import filters

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize language detector
DetectorFactory.seed = 0

def detect_languages(text, min_length=50):
    """
    Detect multiple languages in text by splitting it into chunks
    and detecting language for each chunk
    """
    languages = set()
    
    # Split text into paragraphs
    paragraphs = [p for p in text.split('\n\n') if len(p.strip()) >= min_length]
    
    for paragraph in paragraphs:
        try:
            lang = detect(paragraph)
            languages.add(lang)
        except:
            continue
    
    # Map language codes to Tesseract codes
    lang_map = {
        'en': 'eng',
        'ar': 'ara',
        'es': 'spa',
        'fr': 'fra',
        'de': 'deu',
        'it': 'ita',
        'ru': 'rus',
        'zh': 'chi_sim',
        'ja': 'jpn',
        'ko': 'kor'
    }
    
    return [lang_map.get(lang, 'eng') for lang in languages]

def enhance_image(image):
    """
    تحسين جودة الصورة لتحسين نتائج OCR
    """
    # تحويل الصورة إلى مصفوفة numpy
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image

    # تحويل إلى صورة رمادية
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    else:
        gray = img_array

    # تصحيح انحراف الصورة
    angle = determine_skew(gray)
    if angle:
        (h, w) = gray.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        gray = cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # تحسين التباين
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # إزالة الضوضاء
    denoised = cv2.fastNlMeansDenoising(gray)

    # تحسين حدة الصورة
    sharpened = filters.unsharp_mask(denoised, radius=1.5, amount=1.5)
    
    # تحويل النتيجة إلى صورة PIL
    enhanced_image = Image.fromarray((sharpened * 255).astype(np.uint8))
    
    # تحسين نهائي للسطوع والتباين
    enhancer = ImageEnhance.Contrast(enhanced_image)
    enhanced_image = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Brightness(enhanced_image)
    enhanced_image = enhancer.enhance(1.2)
    
    return enhanced_image

def preprocess_image_for_ocr(image):
    """
    تجهيز الصورة لعملية OCR
    """
    # تطبيق التحسينات الأساسية
    enhanced = enhance_image(image)
    
    # تحويل الصورة إلى أبيض وأسود باستخدام عتبة تكيفية
    img_array = np.array(enhanced)
    binary = cv2.adaptiveThreshold(
        img_array,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    
    return Image.fromarray(binary)

def format_text(text, format_options):
    """Format text based on selected options"""
    try:
        # Apply line spacing
        if format_options.get('line_spacing'):
            text = '\n'.join([line + '\n' for line in text.split('\n')])
            
        # Apply margins
        if format_options.get('margins'):
            text = '\n'.join(['    ' + line for line in text.split('\n')])
            
        return text
    except Exception as e:
        logger.error(f"Error formatting text: {str(e)}")
        return text

def correct_text(text, langs):
    """Apply text corrections based on detected languages"""
    try:
        corrected_text = ""
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                corrected_text += '\n\n'
                continue
                
            try:
                # Detect language of paragraph
                lang = detect(paragraph)
                
                if lang == 'ar':
                    # Handle Arabic text
                    reshaped_text = arabic_reshaper.reshape(paragraph)
                    paragraph = get_display(reshaped_text)
                elif lang in ['en', 'es', 'fr', 'de', 'it']:
                    # Spell check for supported languages
                    blob = TextBlob(paragraph)
                    paragraph = str(blob.correct())
                
                corrected_text += paragraph + '\n\n'
            except:
                corrected_text += paragraph + '\n\n'
        
        return corrected_text.strip()
    except Exception as e:
        logger.error(f"Error correcting text: {str(e)}")
        return text
