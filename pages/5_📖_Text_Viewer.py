import streamlit as st
from pathlib import Path
import sys
import os

# Add the root directory to the Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from ui.components import init_session_state, set_page_config
from utils.pdf_processing import get_page_image

# Initialize session state and set page config
init_session_state()
set_page_config()

def main():
    st.title("عرض النص المستخرج ")
    
    if not st.session_state.converted_pages:
        st.warning("لا يوجد نص مستخرج بعد. الرجاء تحويل ملف PDF أولاً.")
        if st.button("العودة إلى الصفحة الرئيسية"):
            st.switch_page("streamlit_app.py")
        return
    
    # Add navigation buttons at the top
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("العودة إلى الصفحة الرئيسية"):
            st.switch_page("streamlit_app.py")
    with col2:
        if st.button("مسح النتائج"):
            st.session_state.converted_pages = []
            st.session_state.current_pdf_path = None
            st.experimental_rerun()
    
    # Show total number of pages
    total_pages = len(st.session_state.converted_pages)
    st.write(f"عدد الصفحات: {total_pages}")
    
    # Add page selector
    page_number = st.selectbox(
        "اختر الصفحة",
        range(1, total_pages + 1),
        format_func=lambda x: f"الصفحة {x}"
    )
    
    # Create tabs for the selected page
    text_tab, image_tab = st.tabs(["النص", "الصورة"])
    
    with text_tab:
        # Show text for the selected page
        st.markdown("### النص المستخرج")
        page_text = st.session_state.converted_pages[page_number - 1]
        st.text_area(
            "نص الصفحة",
            value=page_text,
            height=400,
            key=f"text_area_{page_number}"
        )
        
        # Add copy button
        if st.button("نسخ النص", key=f"copy_btn_{page_number}"):
            st.write("تم نسخ النص!")
            st.toast("تم نسخ النص بنجاح!")
    
    with image_tab:
        # Show image for the selected page
        st.markdown("### صورة الصفحة")
        if st.session_state.current_pdf_path:
            try:
                image = get_page_image(st.session_state.current_pdf_path, page_number - 1)
                if image:
                    st.image(image, caption=f"الصفحة {page_number}", use_column_width=True)
                else:
                    st.warning("لا يمكن عرض صورة الصفحة")
            except Exception as e:
                st.error(f"حدث خطأ أثناء تحميل صورة الصفحة: {str(e)}")
    
    # Add page navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if page_number > 1:
            if st.button("الصفحة السابقة"):
                st.session_state.page_number = page_number - 1
                st.experimental_rerun()
    
    with col2:
        st.write(f"الصفحة {page_number} من {total_pages}")
    
    with col3:
        if page_number < total_pages:
            if st.button("الصفحة التالية"):
                st.session_state.page_number = page_number + 1
                st.experimental_rerun()

if __name__ == "__main__":
    main()
