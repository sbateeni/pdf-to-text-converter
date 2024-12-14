import logging
from pathlib import Path
from docx import Document
from mdutils.mdutils import MdUtils
import tempfile
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_uploaded_file(uploaded_file):
    """
    حفظ الملف المرفوع في مجلد مؤقت وإرجاع المسار
    """
    try:
        # إنشاء مجلد مؤقت إذا لم يكن موجوداً
        temp_dir = Path(tempfile.gettempdir()) / "pdf_converter"
        temp_dir.mkdir(exist_ok=True)
        
        # إنشاء مسار للملف المؤقت
        file_path = temp_dir / uploaded_file.name
        
        # حفظ الملف
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        return str(file_path)
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}")
        raise

def create_docx(text, output_path):
    """Create a DOCX file from text"""
    try:
        doc = Document()
        doc.add_paragraph(text)
        doc.save(output_path)
        return True
    except Exception as e:
        logger.error(f"Error creating DOCX: {str(e)}")
        raise

def format_output(text, output_format, metadata=None):
    """Format text based on output format"""
    try:
        if output_format == 'md':
            md = MdUtils(file_name='output')
            
            # Add metadata if available
            if metadata and isinstance(metadata, dict):
                md.new_header(1, "Document Information")
                for key, value in metadata.items():
                    md.new_line(f"**{key}:** {value}")
                md.new_line("\n---\n")
            
            md.new_header(1, "Extracted Text")
            md.new_paragraph(text)
            return md.get_md_text()
        
        elif output_format == 'html':
            html = ["<html><head><style>",
                   "body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }",
                   "h1 { color: #333; }",
                   ".metadata { background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }",
                   ".content { white-space: pre-wrap; }",
                   "</style></head><body>"]
            
            # Add metadata if available
            if metadata and isinstance(metadata, dict):
                html.append("<div class='metadata'><h1>Document Information</h1>")
                for key, value in metadata.items():
                    html.append(f"<p><strong>{key}:</strong> {value}</p>")
                html.append("</div>")
            
            html.extend([
                "<h1>Extracted Text</h1>",
                f"<div class='content'>{text}</div>",
                "</body></html>"
            ])
            
            return "\n".join(html)
        
        return text
    
    except Exception as e:
        logger.error(f"Error formatting output: {str(e)}")
        return text
