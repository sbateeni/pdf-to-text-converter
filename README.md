# PDF to Text Converter

متوفر مباشرة على: [https://pdf-to-text-converter.streamlit.app](https://pdf-to-text-converter.streamlit.app)

أداة متعددة الوظائف لتحويل ملفات PDF إلى نص مع دعم للغة العربية والعديد من اللغات الأخرى. تقوم الأداة بتحويل PDF إلى صور، واستخراج النص باستخدام OCR، وحفظ النص المستخرج بتنسيقات مختلفة.

## المميزات الرئيسية

- دعم كامل للغة العربية والإنجليزية والفرنسية والإسبانية وغيرها
- تحويل صفحات PDF إلى صور عالية الجودة
- استخراج النص باستخدام Tesseract OCR
- تصحيح الأخطاء الإملائية للنص الإنجليزي
- دعم اتجاه النص من اليمين إلى اليسار للغة العربية
- عرض الصور والنص المستخرج
- حفظ النص المستخرج بتنسيقات Word وPDF وMarkdown
- تحويل النص المستخرج إلى كلام
- تحويل متعدد التنسيقات (HTML، RTF، YAML، JSON، CSV، Excel، PowerPoint)

## الميزات الجديدة
- اختيار الصوت لتحويل النص إلى كلام
- تصدير النص المستخرج إلى تنسيق Markdown
- تحسين تسجيل الأخطاء للتصحيح
- دعم متعدد اللغات
- تحويل الصور إلى نص
- تحويل PDF إلى صور
- معالجة محتوى HTML
- تحسين جودة الصور قبل OCR
- دعم ملفات PDF المحمية
- واجهة مستخدم محسنة وسهلة الاستخدام

## التثبيت المحلي

1. استنساخ المستودع:
    ```bash
    git clone https://github.com/XmaX111/pdf-to-text-converter.git
    ```

2. الانتقال إلى مجلد المشروع:
    ```bash
    cd pdf-to-text-converter
    ```

3. تثبيت الحزم المطلوبة:
    ```bash
    pip install -r requirements.txt
    ```

## الاستخدام

1. تشغيل التطبيق محلياً:
    ```bash
    streamlit run streamlit_app.py
    ```

2. أو استخدام النسخة المباشرة على:
   [https://pdf-to-text-converter.streamlit.app](https://pdf-to-text-converter.streamlit.app)

3. لتحويل PDF:
   - قم برفع ملف PDF
   - اختر لغة النص للتعرف الضوئي
   - حدد اتجاه النص
   - حدد نطاق الصفحات (اختياري)
   - فعّل تصحيح الإملاء (اختياري)
   - اختر عرض الصور (اختياري)

4. انقر على زر التحويل المناسب لمعالجة المستند.

5. قم بتحميل الملف المحول أو عرض المحتوى المستخرج.

## الأدوات الإضافية

- البحث في النص: البحث داخل النص المستخرج
- عارض الصور: عرض الصور المستخرجة من ملفات PDF
- محدد اللغة: اختيار لغة واجهة المستخدم المفضلة
- الإعدادات: تكوين إعدادات التطبيق
- سجل الأخطاء: عرض وإدارة سجلات الأخطاء

## الترخيص

هذا المشروع مرخص تحت رخصة MIT. راجع ملف [LICENSE](LICENSE) للتفاصيل.

## التواصل

للأسئلة أو المشكلات، يرجى التواصل عبر [GitHub Issues](https://github.com/XmaX111/pdf-to-text-converter/issues).
