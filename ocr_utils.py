import os
import requests
import pytesseract
import tempfile
import shutil

def download_tessdata(lang_code, tessdata_dir):
    url = f'https://github.com/tesseract-ocr/tessdata_fast/raw/main/{lang_code}.traineddata'
    try:
        response = requests.get(url, timeout=10)  # Increased timeout
        response.raise_for_status()  # Raise an error for bad responses
        with open(os.path.join(tessdata_dir, f'{lang_code}.traineddata'), 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {lang_code}: {e}")  # Handle the error
        # Optionally, you can implement a retry mechanism here

def setup_tesseract(languages=['eng', 'ara', 'spa']):
    tessdata_dir = os.path.join(tempfile.gettempdir(), 'tessdata')

    if not os.path.exists(tessdata_dir):
        os.makedirs(tessdata_dir)

    for lang in languages:
        if not os.path.exists(os.path.join(tessdata_dir, f'{lang}.traineddata')):
            download_tessdata(lang, tessdata_dir)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    os.environ['TESSDATA_PREFIX'] = tessdata_dir

# Clear the Cache
comtypes_gen_path = r'C:\Users\XmaX\AppData\Local\Programs\Python\Python312\Lib\site-packages\comtypes\gen'
if os.path.exists(comtypes_gen_path):
    shutil.rmtree(comtypes_gen_path)  # Remove the entire gen directory
