import pytest
from pages.utils import extract_text_from_pdf

def test_extract_text_from_pdf():
    # اختبار استخراج النص من ملف PDF
    result = extract_text_from_pdf("test.pdf")
    assert isinstance(result, str)  # التأكد من أن الناتج نص