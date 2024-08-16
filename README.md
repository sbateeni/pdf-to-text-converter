# PDF to text Converter
#####
This project converts PDF files to images, extracts text using OCR, and saves the extracted text to Word or PDF files.

## Features

- Convert PDF pages to images
- Extract text using Tesseract OCR
- Correct spelling for English text
- Reverse text direction for RTL languages
- Display images and extracted text
- Save extracted text to Word or PDF files

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/pdf-to-image-converter.git
    ```

2. Navigate to the project directory:
    ```bash
    cd pdf-to-image-converter
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

2. Upload a PDF file and configure settings:
    - Select language for OCR
    - Choose text direction
    - Specify page range (optional)
    - Enable spell checking (optional)
    - Display images (optional)

3. Click "Convert" to process the PDF and extract text.

4. Optionally, save the extracted text to Word or PDF using the provided buttons.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [Your Name](mailto:your.email@example.com).

