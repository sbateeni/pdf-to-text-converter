import streamlit as st
import os
from pathlib import Path

def display_converted_text():
    if 'converted_pages' in st.session_state:
        st.title("النص المستخرج من PDF")
        
        # Create tabs for each page
        page_tabs = st.tabs([f"صفحة {i+1}" for i in range(len(st.session_state.converted_pages))])
        
        # Display text for each page in its respective tab
        for i, (tab, page_text) in enumerate(zip(page_tabs, st.session_state.converted_pages)):
            with tab:
                st.text_area(
                    label=f"نص الصفحة {i+1}",
                    value=page_text,
                    height=400,
                    key=f"text_area_{i}"
                )
                
                # If there's a corresponding image, display it
                image_path = f"{st.session_state.get('current_pdf_path', '')}_page_{i+1}.png"
                if os.path.exists(image_path):
                    with st.expander("عرض الصورة الأصلية"):
                        st.image(image_path)
    else:
        st.info("لم يتم تحويل أي ملف PDF بعد. الرجاء العودة إلى الصفحة الرئيسية وتحويل ملف PDF أولاً.")

if __name__ == "__main__":
    display_converted_text()
