import streamlit as st
import yaml
import json

def convert_yaml_to_json(yaml_file):
    """Convert YAML file to JSON."""
    data = yaml.safe_load(yaml_file)
    json_file_path = "output.json"
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    return json_file_path

def show():
    st.title("📄 Convert YAML to JSON")

    uploaded_file = st.file_uploader("📂 Choose a YAML file", type=["yaml", "yml"])

    if uploaded_file:
        if st.button("📝 Convert YAML to JSON"):
            try:
                json_file_path = convert_yaml_to_json(uploaded_file)
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