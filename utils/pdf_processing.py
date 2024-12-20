import logging
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import os

from utils.text_processing import (
    detect_languages,
    enhance_image,
    correct_text,
    preprocess_image_for_ocr,
    convert_to_tesseract_langs
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_page_range(page_range, total_pages=None):
    """Parse page range string into list of page numbers"""
    if not page_range:
        return range(total_pages) if total_pages is not None else []
    
    pages_to_process = set()
    ranges = page_range.replace(' ', '').split(',')
    
    for r in ranges:
        if '-' in r:
            start, end = map(int, r.split('-'))
            # Convert to 0-based index
            start = max(0, start - 1)
            end = min(total_pages, end) if total_pages else end
            pages_to_process.update(range(start, end))
        else:
            # Convert to 0-based index
            page = int(r) - 1
            if 0 <= page < (total_pages or float('inf')):
                pages_to_process.add(page)
    
    return sorted(pages_to_process)

def extract_text_from_image(image, languages):
    """
    استخراج النص من الصورة باستخدام OCR
    """
    try:
        # تحسين جودة الصورة
        preprocessed_image = preprocess_image_for_ocr(image)
        
        # تحويل قائمة اللغات إلى تنسيق tesseract
        lang_codes = convert_to_tesseract_langs(languages)
        lang_string = '+'.join(lang_codes)
        
        # إعداد خيارات tesseract
        custom_config = r'--oem 3 --psm 6'
        
        # تنفيذ OCR
        text = pytesseract.image_to_string(
            preprocessed_image, 
            lang=lang_string,
            config=custom_config
        )
        
        return text.strip()
    except Exception as e:
        logger.error(f"Error in OCR processing: {str(e)}")
        return ""

def extract_text_from_pdf(pdf_path, page_range=None, detect_lang=True, manual_langs=None):
    """Extract text from PDF using PyPDF2"""
    try:
        text = ""
        pdf_reader = PdfReader(pdf_path)
        total_pages = len(pdf_reader.pages)
        
        # Get pages to process
        pages_to_process = parse_page_range(page_range, total_pages)
        
        # Dictionary to store detected languages for each page
        page_languages = {}
        
        for page_num in pages_to_process:
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            
            if detect_lang:
                # Detect languages in the page text
                langs = detect_languages(page_text)
                page_languages[page_num] = langs
            elif manual_langs:
                page_languages[page_num] = manual_langs
            
            # Apply language-specific processing
            if page_num in page_languages:
                page_text = correct_text(page_text, page_languages[page_num])
            
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page_text + "\n"
        
        # Perform OCR on pages that do not have extractable text
        images = convert_from_path(pdf_path)
        for page_num in pages_to_process:
            if not page_text.strip():
                image = images[page_num]
                page_text = extract_text_from_image(image, page_languages.get(page_num, ['eng']))
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page_text + "\n"
        
        return text.strip(), total_pages, page_languages
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def perform_ocr(pdf_path, page_range=None, detect_lang=True, manual_langs=None, enhance_images=False):
    """Perform OCR on PDF pages"""
    try:
        # تحويل PDF إلى صور
        images = convert_from_path(
            pdf_path,
            fmt='ppm',
            grayscale=True,
            size=(1700, None)  # تحسين الدقة
        )
        
        # تحديد الصفحات المطلوبة
        pages_to_process = parse_page_range(page_range, len(images))
        
        # معالجة كل صفحة
        text = ""
        processed_images = []
        
        for page_num in pages_to_process:
            if page_num >= len(images):
                continue
                
            image = images[page_num]
            
            # تحسين جودة الصورة إذا تم تفعيل الخيار
            if enhance_images:
                image = enhance_image(image)
            
            # تجهيز الصورة لـ OCR
            image = preprocess_image_for_ocr(image)
            processed_images.append(image)
            
            # تحديد اللغات
            if detect_lang:
                # استخراج عينة من النص للكشف عن اللغة
                sample_langs = pytesseract.image_to_string(image, lang='eng+ara')
                langs = detect_languages(sample_langs)
            else:
                langs = manual_langs or ['eng']
            
            # استخراج النص
            page_text = extract_text_from_image(image, langs)
            
            # تصحيح النص
            page_text = correct_text(page_text, langs)
            
            text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
        
        return text.strip(), processed_images
        
    except Exception as e:
        logger.error(f"Error performing OCR: {str(e)}")
        raise

def convert_pdf_to_images_and_text(pdf_path, page_range=None, languages=None):
    """
    تحويل PDF إلى صور ثم إلى نص باستخدام OCR
    """
    try:
        # تحويل PDF إلى صور
        images = convert_from_path(pdf_path)
        total_pages = len(images)
        
        # تحويل نطاق الصفحات إلى قائمة
        pages_to_process = parse_page_range(page_range, total_pages)
        
        # تحديد الصفحات للمعالجة
        if not pages_to_process:
            pages_to_process = list(range(total_pages))
        else:
            pages_to_process = [p for p in pages_to_process if p < total_pages]
        
        text = ""
        page_languages = {}
        
        # معالجة كل صفحة
        for page_num in pages_to_process:
            image = images[page_num]
            
            # تحسين جودة الصورة
            enhanced_image = preprocess_image_for_ocr(image)
            
            # استخراج النص من الصورة
            if languages:
                current_langs = languages
            else:
                # Use default languages for OCR
                current_langs = ['eng', 'ara']  # Default to English and Arabic
            
            page_text = extract_text_from_image(enhanced_image, current_langs)
            
            # Try to detect languages from extracted text
            try:
                detected_langs = detect_languages(page_text)
                page_languages[page_num] = detected_langs
            except Exception as e:
                logger.warning(f"Could not detect languages for page {page_num + 1}: {str(e)}")
                page_languages[page_num] = current_langs
            
            # إضافة النص مع رقم الصفحة
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page_text + "\n"
            
            # حفظ الصورة
            image_path = f"{pdf_path}_page_{page_num + 1}.png"
            enhanced_image.save(image_path, "PNG")
        
        return text.strip(), total_pages, page_languages, pages_to_process
    except Exception as e:
        logger.error(f"Error converting PDF to images and text: {str(e)}")
        raise
