import streamlit as st
import pandas as pd

def convert_csv_to_excel(csv_file):
    """Convert CSV file to Excel."""
    df = pd.read_csv(csv_file)
    excel_file_path = "output.xlsx"
    df.to_excel(excel_file_path, index=False)
    return excel_file_path

def show():
    st.title("📄 Convert CSV to Excel")

    uploaded_file = st.file_uploader("📂 Choose a CSV file", type=["csv"])

    if uploaded_file:
        if st.button("📝 Convert CSV to Excel"):
            try:
                excel_file_path = convert_csv_to_excel(uploaded_file)
                st.success("✅ Conversion completed!")

                with open(excel_file_path, "rb") as excel_file:
                    st.download_button(
                        label="📥 Download Excel Document",
                        data=excel_file.read(),
                        file_name="output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"❌ An error occurred during conversion: {str(e)}")

if __name__ == "__main__":
    show()