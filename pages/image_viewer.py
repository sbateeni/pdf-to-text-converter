import streamlit as st

def show():
    st.title("🖼️ Image Viewer")

    # Initialize session state for extracted_images
    if 'extracted_images' not in st.session_state:
        st.session_state['extracted_images'] = []

    if st.session_state['extracted_images']:
        if st.button("عرض الصور"):
            for i, image in enumerate(st.session_state['extracted_images']):
                st.image(image, caption=f"Page {i + 1}")
    else:
        st.error("⚠️ No images available. Please convert a PDF first.")
