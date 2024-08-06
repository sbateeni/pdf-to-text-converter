from textblob import TextBlob
import arabic_reshaper
from bidi.algorithm import get_display

def correct_spelling(text, lang_code):
    if lang_code == 'ara':
        # إعادة تشكيل النص العربي
        reshaped_text = arabic_reshaper.reshape(text)
        # عكس النص ليظهر بشكل صحيح
        corrected_text = get_display(reshaped_text)
        return corrected_text
    elif lang_code == 'eng' or lang_code == 'spa':
        blob = TextBlob(text)
        corrected_text = str(blob.correct())
        return corrected_text
    return text
