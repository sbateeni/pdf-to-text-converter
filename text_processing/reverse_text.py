import arabic_reshaper
from bidi.algorithm import get_display

def reverse_text(text, lang):
    if lang == 'ara':  # Only reshape if the language is Arabic
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    return text
