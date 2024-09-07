import streamlit as st
import logging

# إعداد تسجيل الأخطاء
logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

def show():
    st.title("🛠️ Error Log")
    
    try:
        with open("error_log.txt", "r") as file:
            logs = file.readlines()
            if logs:
                st.subheader("Recent Errors:")
                for log in logs:
                    st.text(log)
            else:
                st.success("No errors logged.")
    except FileNotFoundError:
        st.error("Error log file not found.")

def log_error(error_message):
    logging.error(error_message)

if __name__ == "__main__":
    show()