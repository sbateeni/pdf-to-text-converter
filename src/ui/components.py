import streamlit as st

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

def create_sidebar():
    """Create sidebar with navigation and theme toggle"""
    with st.sidebar:
        st.title("Navigation")
        st.write("Additional Tools:")
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
    tabs = st.tabs(["OCR & Language", "Image Enhancement", "Text Formatting"])
    
    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            use_ocr = st.checkbox(
                "Use OCR",
                value=st.session_state.settings['use_ocr'],
                key='use_ocr'
            )
        with col2:
            create_language_settings()
    
    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            enhance_images = st.checkbox(
                "Enhance image quality",
                value=st.session_state.settings['enhance_images'],
                key='enhance_images'
            )
            preview_enhanced = st.checkbox(
                "Preview enhanced images",
                value=st.session_state.settings['preview_enhanced'],
                key='preview_enhanced'
            )
        with col2:
            correct_spelling = st.checkbox(
                "Correct spelling",
                value=st.session_state.settings['correct_spelling'],
                key='correct_spelling'
            )
            remove_extra_spaces = st.checkbox(
                "Remove extra spaces",
                value=st.session_state.settings['remove_extra_spaces'],
                key='remove_extra_spaces'
            )
    
    with tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            line_spacing = st.checkbox(
                "Double line spacing",
                value=st.session_state.settings['line_spacing'],
                key='line_spacing'
            )
            add_margins = st.checkbox(
                "Add margins",
                value=st.session_state.settings['add_margins'],
                key='add_margins'
            )
        with col2:
            output_format = st.selectbox(
                "Output format",
                options=['txt', 'md', 'html', 'docx'],
                format_func=lambda x: {
                    'txt': 'Plain Text',
                    'md': 'Markdown',
                    'html': 'HTML',
                    'docx': 'Word Document'
                }[x],
                key='output_format'
            )

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
