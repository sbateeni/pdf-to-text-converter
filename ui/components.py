import streamlit as st
import os
import glob
from pathlib import Path
from utils.pdf_processing import convert_pdf_to_images_and_text
from utils.text_processing import format_text

def init_session_state():
    """Initialize session state with default values"""
    if 'settings' not in st.session_state:
        st.session_state.settings = {
            'use_ocr': True,
            'auto_detect_lang': True,
            'manual_langs': ['eng'],
            'enhance_images': True,
            'preview_enhanced': False,
            'correct_spelling': True,
            'remove_extra_spaces': True,
            'line_spacing': False,
            'add_margins': False,
            'output_format': 'txt'
        }
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    if 'converted_pages' not in st.session_state:
        st.session_state.converted_pages = []
    if 'current_pdf_path' not in st.session_state:
        st.session_state.current_pdf_path = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False

def create_sidebar():
    """Create sidebar with navigation and theme toggle"""
    with st.sidebar:
        st.title("Navigation")
        st.write("Additional Tools:")
        
        # Using relative paths for page links
        st.page_link("pages/1_🔍_OCR.py", label="OCR Processing", icon="🔍")
        st.page_link("pages/2_📝_Text_Editor.py", label="Text Editor", icon="📝")
        st.page_link("pages/3_📊_Text_Analysis.py", label="Text Analysis", icon="📊")
        st.page_link("pages/4_📑_Document_Analysis.py", label="Document Analysis", icon="📑")
        
        st.divider()
        st.write("Settings:")
        theme_toggle = st.button(
            "Toggle Dark/Light Theme",
            on_click=toggle_theme
        )

def create_language_settings():
    """Create language selection interface"""
    col1, col2 = st.columns(2)
    
    with col1:
        auto_detect = st.checkbox(
            "Auto-detect language",
            value=st.session_state.settings['auto_detect_lang'],
            key='auto_detect_lang'
        )
    
    with col2:
        # Multi-language selection
        available_langs = {
            'eng': 'English',
            'ara': 'Arabic',
            'spa': 'Spanish',
            'fra': 'French',
            'deu': 'German',
            'ita': 'Italian',
            'rus': 'Russian',
            'chi_sim': 'Chinese (Simplified)',
            'jpn': 'Japanese',
            'kor': 'Korean'
        }
        
        manual_langs = st.multiselect(
            "Select document languages",
            options=list(available_langs.keys()),
            default=st.session_state.settings['manual_langs'],
            format_func=lambda x: available_langs[x],
            disabled=auto_detect,
            key='manual_langs'
        )
        
        if not auto_detect and not manual_langs:
            st.warning("Please select at least one language")
            manual_langs = ['eng']
        
        st.session_state.settings['manual_langs'] = manual_langs

def create_processing_tabs():
    """Create tabs for different processing options"""
    # Create three columns for the control buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("تحويل PDF إلى نص", type="primary"):
            if 'current_pdf_path' in st.session_state and st.session_state.current_pdf_path:
                st.session_state.processing = True
                process_pdf()
            else:
                st.error("الرجاء تحميل ملف PDF أولاً")
    
    with col2:
        if st.button("عرض النص المستخرج"):
            st.switch_page("pages/5_📖_Text_Viewer.py")
    
    with col3:
        if st.button("مسح النتائج"):
            clear_results()

    # Only show processing options if not currently processing
    if not st.session_state.get('processing', False):
        # Add page range selection at the top
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            process_all = st.checkbox("تحويل كل الصفحات", value=True, key='process_all')
        
        if not process_all:
            with col2:
                page_range = st.text_input(
                    "حدد نطاق الصفحات (مثال: 1-3 أو 1,2,3 أو 1-3,5-7)",
                    help="""
                    يمكنك تحديد الصفحات بعدة طرق:
                    - رقم واحد: مثل '5' لتحويل الصفحة الخامسة فقط
                    - نطاق: مثل '1-3' لتحويل الصفحات من 1 إلى 3
                    - قائمة: مثل '1,3,5' لتحويل صفحات محددة
                    - مزيج: مثل '1-3,5,7-9' لتحويل مجموعة من النطاقات والصفحات
                    """
                )
        else:
            page_range = None

        tab1, tab2, tab3 = st.tabs(["إعدادات OCR", "تحسين النص", "إعدادات الإخراج"])
        
        with tab1:
            st.session_state.settings['use_ocr'] = st.toggle("استخدام OCR", value=st.session_state.settings['use_ocr'])
            st.session_state.settings['auto_detect_lang'] = st.toggle("كشف تلقائي للغة", value=st.session_state.settings['auto_detect_lang'])
            if not st.session_state.settings['auto_detect_lang']:
                st.session_state.settings['manual_langs'] = st.multiselect(
                    "اختر اللغات",
                    ['eng', 'ara', 'fra', 'deu'],
                    default=st.session_state.settings['manual_langs']
                )
            st.session_state.settings['enhance_images'] = st.toggle("تحسين جودة الصور", value=st.session_state.settings['enhance_images'])
            
        with tab2:
            st.session_state.settings['correct_spelling'] = st.toggle("تصحيح الإملاء", value=st.session_state.settings['correct_spelling'])
            st.session_state.settings['remove_extra_spaces'] = st.toggle("إزالة المسافات الزائدة", value=st.session_state.settings['remove_extra_spaces'])
            
        with tab3:
            st.session_state.settings['line_spacing'] = st.toggle("تباعد الأسطر", value=st.session_state.settings['line_spacing'])
            st.session_state.settings['add_margins'] = st.toggle("إضافة هوامش", value=st.session_state.settings['add_margins'])
            st.session_state.settings['output_format'] = st.selectbox(
                "تنسيق الإخراج",
                ['txt', 'docx', 'pdf'],
                index=['txt', 'docx', 'pdf'].index(st.session_state.settings['output_format'])
            )

def process_pdf():
    """Process the PDF file and store results"""
    try:
        if st.session_state.current_pdf_path:
            with st.spinner("جاري تحويل PDF إلى نص..."):
                # Get page range if specified
                page_range = None if st.session_state.get('process_all', True) else st.session_state.get('page_range', '')
                
                # Convert PDF to images and text
                text, total_pages, page_languages, pages_processed = convert_pdf_to_images_and_text(
                    st.session_state.current_pdf_path,
                    page_range=page_range,
                    languages=st.session_state.settings['manual_langs'] if not st.session_state.settings['auto_detect_lang'] else None
                )
                
                # Format text if needed
                if st.session_state.settings['remove_extra_spaces']:
                    text = " ".join(text.split())
                
                # Split text into pages and store in session state
                pages = text.split('\n--- Page')
                st.session_state.converted_pages = [page.strip() for page in pages if page.strip()]
                
                # Show success message with page information
                if page_range:
                    st.success(f"تم تحويل {len(pages_processed)} صفحات من أصل {total_pages} صفحة!")
                else:
                    st.success(f"تم تحويل {total_pages} صفحات بنجاح!")
                
                st.button("عرض النتائج", on_click=lambda: st.switch_page("pages/5_📖_Text_Viewer.py"))
    except Exception as e:
        st.error(f"حدث خطأ أثناء المعالجة: {str(e)}")
    finally:
        st.session_state.processing = False

def clear_results():
    """Clear all conversion results and temporary files"""
    if 'current_pdf_path' in st.session_state:
        # Delete temporary image files
        import glob
        for img_file in glob.glob(f"{st.session_state.current_pdf_path}_page_*.png"):
            try:
                os.remove(img_file)
            except:
                pass
    
    # Clear session state
    st.session_state.converted_pages = []
    st.session_state.current_pdf_path = None
    st.session_state.processing = False
    st.success("تم مسح جميع النتائج")

def toggle_theme():
    """Toggle between light and dark theme"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

def apply_theme():
    """Apply current theme"""
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stTextInput, .stSelectbox, .stMultiselect {
            background-color: #2D2D2D;
            color: #FFFFFF;
        }
        </style>
        """, unsafe_allow_html=True)

def display_results(text, metadata=None, images=None, page_range=None):
    """Display extracted text and related information"""
    if not text:
        return
    
    # عرض معلومات المستند
    if metadata:
        st.subheader("Document Information")
        for key, value in metadata.items():
            st.text(f"{key}: {value}")
        st.divider()
    
    # عرض النص المستخرج
    st.subheader("Extracted Text")
    st.text_area("", value=text, height=400)
    
    # عرض الصور المعالجة
    if images and st.session_state.settings.get('preview_enhanced', False):
        st.subheader("Processed Images")
        
        # Get pages to preview
        if page_range:
            from src.utils.pdf_processing import parse_page_range
            preview_pages = parse_page_range(page_range, len(images))
            for page_num in preview_pages:
                st.image(images[page_num], caption=f"Page {page_num + 1}")
        else:
            for i, image in enumerate(images):
                st.image(image, caption=f"Page {i + 1}")
    
    # عرض خيارات التحميل
    st.subheader("Download Options")
    output_format = st.session_state.settings.get('output_format', 'txt')
    
    if output_format == 'txt':
        st.download_button(
            "Download Text",
            text,
            "extracted_text.txt",
            "text/plain"
        )
    elif output_format == 'docx':
        from src.utils.file_handling import create_docx
        import tempfile
        
        # إنشاء ملف Word مؤقت
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            create_docx(text, tmp.name)
            
            # تحميل الملف
            with open(tmp.name, 'rb') as f:
                st.download_button(
                    "Download Word Document",
                    f.read(),
                    "extracted_text.docx",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
    elif output_format in ['md', 'html']:
        from src.utils.file_handling import format_output
        
        formatted_text = format_output(text, output_format, metadata)
        st.download_button(
            f"Download {output_format.upper()}",
            formatted_text,
            f"extracted_text.{output_format}",
            f"text/{output_format}"
        )
