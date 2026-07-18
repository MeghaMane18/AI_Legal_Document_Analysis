import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path

# Configure only on Windows
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    POPPLER_PATH = (
        r"C:\Users\om\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
    )
else:
    POPPLER_PATH = None


def extract_text(file_path):

    text = ""

    print("Extracting text using pdfplumber...")

    try:
        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print(e)

    if len(text.strip()) > 50:
        print("Text extracted successfully.")
        return text.strip()

    print("Running OCR...")

    try:

        if POPPLER_PATH:
            images = convert_from_path(
                file_path,
                poppler_path=POPPLER_PATH
            )
        else:
            images = convert_from_path(file_path)

        text = ""

        for image in images:
            text += pytesseract.image_to_string(image)

        return text.strip()

    except Exception as e:

        print("OCR Failed:", e)

        return ""