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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize language detector
DetectorFactory.seed = 0

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    logger.warning("OpenCV not available. Using basic image processing.")

def convert_to_tesseract_langs(languages):
    """
    تحويل قائمة اللغات إلى رموز لغات Tesseract
    """
    lang_map = {
        'ar': 'ara',    # العربية
        'en': 'eng',    # الإنجليزية
        'fr': 'fra',    # الفرنسية
        'de': 'deu',    # الألمانية
        'es': 'spa',    # الإسبانية
        'it': 'ita',    # الإيطالية
        'ru': 'rus',    # الروسية
        'zh': 'chi_sim',# الصينية المبسطة
        'ja': 'jpn',    # اليابانية
        'ko': 'kor'     # الكورية
    }
    
    if not languages:
        return ['eng']  # استخدام الإنجليزية كلغة افتراضية
    
    # تحويل كل لغة إلى رمز Tesseract المناسب
    tesseract_langs = []
    for lang in languages:
        if lang in lang_map:
            tesseract_langs.append(lang_map[lang])
        elif lang.lower() in lang_map.values():
            tesseract_langs.append(lang.lower())
    
    # إذا لم يتم العثور على أي لغة صالحة، استخدم الإنجليزية
    return tesseract_langs if tesseract_langs else ['eng']

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
    
    return convert_to_tesseract_langs(languages)

def enhance_image(image):
    """
    تحسين جودة الصورة لتحسين نتائج OCR
    """
    try:
        if OPENCV_AVAILABLE:
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

            # تحسين التباين
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            gray = clahe.apply(gray)

            # إزالة الضوضاء
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # تحويل النتيجة إلى صورة PIL
            enhanced_image = Image.fromarray(denoised)
        else:
            # استخدام معالجة الصور الأساسية من PIL
            enhanced_image = image.convert('L')
            
            # تحسين التباين
            enhancer = ImageEnhance.Contrast(enhanced_image)
            enhanced_image = enhancer.enhance(2.0)
            
            # تحسين الحدة
            enhancer = ImageEnhance.Sharpness(enhanced_image)
            enhanced_image = enhancer.enhance(1.5)
        
        # تحسين نهائي للسطوع والتباين
        enhancer = ImageEnhance.Contrast(enhanced_image)
        enhanced_image = enhancer.enhance(1.5)
        enhancer = ImageEnhance.Brightness(enhanced_image)
        enhanced_image = enhancer.enhance(1.2)
        
        return enhanced_image
    except Exception as e:
        logger.error(f"Error enhancing image: {str(e)}")
        return image

def preprocess_image_for_ocr(image):
    """
    تجهيز الصورة لعملية OCR
    """
    # تطبيق التحسينات الأساسية
    enhanced = enhance_image(image)
    
    if OPENCV_AVAILABLE:
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
    else:
        # استخدام معالجة الصور الأساسية من PIL
        return enhanced.point(lambda x: 0 if x < 128 else 255, '1')

def format_text(text, format_options):
    """Format text based on selected options"""
    formatted_text = text
    
    # Add line spacing
    if format_options.get('line_spacing'):
        formatted_text = '\n'.join([line + '\n' for line in formatted_text.split('\n')])
    
    # Add margins
    if format_options.get('margins'):
        formatted_text = '\n'.join(['    ' + line for line in formatted_text.split('\n')])
    
    return formatted_text

def correct_text(text, langs):
    """Apply text corrections based on detected languages"""
    try:
        # Handle right-to-left languages
        if 'ara' in langs:
            # Reshape Arabic text
            text = arabic_reshaper.reshape(text)
            # Handle bidirectional text
            text = get_display(text)
        
        # Apply spell checking for English text
        if 'eng' in langs:
            blob = TextBlob(text)
            text = str(blob.correct())
        
        return text
    except Exception as e:
        logger.error(f"Error correcting text: {str(e)}")
        return text
