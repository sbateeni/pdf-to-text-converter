import os
import requests
import pytesseract
import tempfile
def download_tessdata(lang_code, tessdata_dir):
    url = f'https://github.com/tesseract-ocr/tessdata_fast/raw/main/{lang_code}.traineddata'
    response = requests.get(url)
    with open(os.path.join(tessdata_dir, f'{lang_code}.traineddata'), 'wb') as f:
        f.write(response.content)

def setup_tesseract(languages=['eng', 'ara', 'spa']):
    tessdata_dir = os.path.join(tempfile.gettempdir(), 'tessdata')

    if not os.path.exists(tessdata_dir):
        os.makedirs(tessdata_dir)

    for lang in languages:
        if not os.path.exists(os.path.join(tessdata_dir, f'{lang}.traineddata')):
            download_tessdata(lang, tessdata_dir)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    os.environ['TESSDATA_PREFIX'] = tessdata_dir
