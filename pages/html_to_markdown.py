import streamlit as st
import html2text

def convert_html_to_markdown(html_content):
    """Convert HTML content to Markdown."""
    return html2text.html2text(html_content)

def show():
    st.title("🌐 Convert HTML to Markdown")

    html_content = st.text_area("Enter HTML content here:")

    if st.button("Convert to Markdown"):
        try:
            markdown_content = convert_html_to_markdown(html_content)
            st.success("✅ Conversion completed!")
            st.text_area("Markdown Output", markdown_content, height=300)
        except Exception as e:
            st.error(f"❌ An error occurred during conversion: {str(e)}")

if __name__ == "__main__":
    show()