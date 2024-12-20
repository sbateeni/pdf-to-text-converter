import streamlit as st
import os
from pathlib import Path

def display_converted_text():
    st.title("النص المستخرج من PDF")
    
    if 'converted_pages' not in st.session_state or not st.session_state.converted_pages:
        st.warning("لم يتم تحويل أي ملف PDF بعد. الرجاء العودة إلى الصفحة الرئيسية وتحويل ملف PDF أولاً.")
        if st.button("العودة إلى الصفحة الرئيسية"):
            st.switch_page("streamlit_app.py")
        return
    
    # Get the number of pages
    num_pages = len(st.session_state.converted_pages)
    
    # Create tabs for each page
    page_tabs = st.tabs([f"صفحة {i+1}" for i in range(num_pages)])
    
    # Display text for each page in its respective tab
    for i, (tab, page_text) in enumerate(zip(page_tabs, st.session_state.converted_pages)):
        with tab:
            # Create columns for text and image
            text_col, image_col = st.columns([2, 1])
            
            with text_col:
                st.text_area(
                    label=f"نص الصفحة {i+1}",
                    value=page_text,
                    height=400,
                    key=f"text_area_{i}"
                )
            
            with image_col:
                # If there's a corresponding image, display it
                if st.session_state.get('current_pdf_path'):
                    image_path = f"{st.session_state.current_pdf_path}_page_{i+1}.png"
                    if os.path.exists(image_path):
                        st.image(image_path, caption=f"الصورة الأصلية - صفحة {i+1}")
    
    # Add navigation buttons at the bottom
    col1, col2 = st.columns(2)
    with col1:
        if st.button("العودة إلى الصفحة الرئيسية"):
            st.switch_page("streamlit_app.py")
    with col2:
        if st.button("مسح النتائج"):
            st.session_state.converted_pages = []
            st.session_state.current_pdf_path = None
            st.rerun()

if __name__ == "__main__":
    display_converted_text()
