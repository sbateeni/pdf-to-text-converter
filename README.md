# PDF to Text Converter

This project is a versatile document conversion tool that primarily converts PDF files to images, extracts text using OCR, and saves the extracted text to various formats including Word, PDF, and Markdown.

## Features

- Convert PDF pages to images
- Extract text using Tesseract OCR
- Correct spelling for English text
- Reverse text direction for RTL languages
- Display images and extracted text
- Save extracted text to Word, PDF, or Markdown formats
- Convert extracted text to speech
- Multiple file format conversions (HTML, RTF, YAML, JSON, CSV, Excel, PowerPoint)

## New Features
- Voice selection for text-to-speech conversion
- Export extracted text to Markdown format
- Improved error logging for better debugging
- Multi-language support (English, Arabic, Spanish, French)
- Image to text conversion
- PDF to image conversion
- HTML content fetching and processing

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/pdf-to-image-converter.git
    ```

2. Navigate to the project directory:
    ```bash
    cd pdf-to-text-converter
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up Tesseract OCR:
    - Download and install Tesseract from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
    - Make sure Tesseract is in your system's PATH.

## Usage

1. Run the application:
    ```bash
    streamlit run app.py
    ```

2. Use the sidebar to navigate between different conversion tools.

3. For PDF conversion:
   - Upload a PDF file
   - Select language for OCR
   - Choose text direction
   - Specify page range (optional)
   - Enable spell checking (optional)
   - Display images (optional)

4. Click the respective conversion button to process your document.

5. Download the converted file or view the extracted content.

## Additional Tools

- Text Search: Search within extracted text
- Image Viewer: View extracted images from PDFs
- Language Selector: Choose your preferred interface language
- Settings: Configure application settings
- Error Log: View and manage error logs

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [Your Name](mailto:your.email@example.com).

