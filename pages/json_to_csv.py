import streamlit as st
import pandas as pd
import json

def convert_json_to_csv(json_file):
    """Convert JSON file to CSV."""
    data = json.load(json_file)
    df = pd.json_normalize(data)
    csv_file_path = "output.csv"
    df.to_csv(csv_file_path, index=False)
    return csv_file_path

def show():
    st.title("📄 Convert JSON to CSV")

    uploaded_file = st.file_uploader("📂 Choose a JSON file", type=["json"])

    if uploaded_file:
        if st.button("📝 Convert JSON to CSV"):
            try:
                csv_file_path = convert_json_to_csv(uploaded_file)
                st.success("✅ Conversion completed!")

                with open(csv_file_path, "rb") as csv_file:
                    st.download_button(
                        label="📥 Download CSV Document",
                        data=csv_file.read(),
                        file_name="output.csv",
                        mime="text/csv"
                    )
            except Exception as e:
                st.error(f"❌ An error occurred during conversion: {str(e)}")

if __name__ == "__main__":
    show()