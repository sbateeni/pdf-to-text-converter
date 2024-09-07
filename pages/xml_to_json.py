import streamlit as st
import xml.etree.ElementTree as ET
import json

def convert_xml_to_json(xml_file):
    """Convert XML file to JSON."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = {root.tag: {}}

    for child in root:
        data[root.tag][child.tag] = child.text

    json_file_path = "output.json"
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    return json_file_path

def show():
    st.title("📄 Convert XML to JSON")

    uploaded_file = st.file_uploader("📂 Choose an XML file", type=["xml"])

    if uploaded_file:
        if st.button("📝 Convert XML to JSON"):
            try:
                json_file_path = convert_xml_to_json(uploaded_file)
                st.success("✅ Conversion completed!")

                with open(json_file_path, "rb") as json_file:
                    st.download_button(
                        label="📥 Download JSON Document",
                        data=json_file.read(),
                        file_name="output.json",
                        mime="application/json"
                    )
            except Exception as e:
                st.error(f"❌ An error occurred during conversion: {str(e)}")

if __name__ == "__main__":
    show()