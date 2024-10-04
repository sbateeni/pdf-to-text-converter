import streamlit as st
from utils import get_translation

# إعداد تسجيل الأخطاء
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

import logging

# إعداد تسجيل الأخطاء
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

def show():
    language = st.session_state.language
    st.title(get_translation("Error Log", language))

    try:
        with open("error_log.txt", "r") as log_file:
            errors = log_file.readlines()
        
        if errors:
            for error in errors:
                st.error(error.strip())
        else:
            st.success(get_translation("No errors logged", language))

        if st.button(get_translation("Clear Error Log", language)):
            open("error_log.txt", "w").close()
            st.success(get_translation("Error log cleared", language))
            st.experimental_rerun()

    except FileNotFoundError:
        st.info(get_translation("No error log file found", language))

def log_error(error_message):
    logging.error(error_message)

if __name__ == "__main__":
    show()