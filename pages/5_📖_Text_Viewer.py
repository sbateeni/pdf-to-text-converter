import streamlit as st
from pathlib import Path
import sys
import os

# Add the root directory to the Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Set up the page
st.set_page_config(
    page_title="عرض النص المستخرج",
    page_icon="📖",
    layout="wide"
)

def main():
    st.title("عرض النص المستخرج 📖")
    
    if not st.session_state.get('converted_pages', []):
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
        format_func=lambda x: f"الصفحة {x}",
        key="page_selector"
    )
    
    # Create tabs for the selected page
    text_tab, image_tab = st.tabs(["النص", "الصورة"])
    
    with text_tab:
        # Show text for the selected page
        st.markdown("### النص المستخرج")
        page_text = st.session_state.converted_pages[page_number - 1]
        text_area = st.text_area(
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
        if st.session_state.get('current_pdf_path'):
            image_path = f"{st.session_state.current_pdf_path}_page_{page_number}.png"
            if os.path.exists(image_path):
                st.image(image_path, caption=f"الصفحة {page_number}", use_column_width=True)
            else:
                st.warning("لا يمكن عرض صورة الصفحة")
    
    # Add page navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if page_number > 1:
            if st.button("الصفحة السابقة"):
                new_page = page_number - 1
                st.session_state.page_selector = new_page
                st.experimental_rerun()
    
    with col2:
        st.write(f"الصفحة {page_number} من {total_pages}")
    
    with col3:
        if page_number < total_pages:
            if st.button("الصفحة التالية"):
                new_page = page_number + 1
                st.session_state.page_selector = new_page
                st.experimental_rerun()

if __name__ == "__main__":
    main()
