import pdfplumber
import pytesseract
from pdf2image import convert_from_path


# ----------------------------------------------------
# Set Tesseract Path
# Change this path if you installed Tesseract elsewhere
# ----------------------------------------------------
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ----------------------------------------------------
# Set Poppler Path
# Change this path to your Poppler bin folder
# ----------------------------------------------------
POPPLER_PATH = r"C:\Users\om\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"


def extract_text(file_path):
    """
    Extract text from PDF.
    First tries pdfplumber.
    If no text is found, automatically performs OCR.
    """

    text = ""

    print("\n========== PDF TEXT EXTRACTION ==========")

    # ------------------------------------------
    # Method 1 : Normal text extraction
    # ------------------------------------------

    try:

        with pdfplumber.open(file_path) as pdf:

            print(f"Total Pages : {len(pdf.pages)}")

            for page_number, page in enumerate(pdf.pages):

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

                else:
                    print(
                        f"Page {page_number + 1}: No selectable text found."
                    )

    except Exception as e:

        print("pdfplumber Error:", e)

    # If enough text was extracted, return it
    if len(text.strip()) > 50:

        print("✅ Text extracted using pdfplumber.")
        print("Characters:", len(text))

        return text.strip()

    # ------------------------------------------
    # Method 2 : OCR
    # ------------------------------------------

    print("\nNo selectable text found.")
    print("Starting OCR...")

    text = ""

    try:

        images = convert_from_path(
            file_path,
            poppler_path=POPPLER_PATH
        )

        for page_number, image in enumerate(images):

            print(f"OCR Page {page_number + 1}")

            page_text = pytesseract.image_to_string(
                image,
                lang="eng"
            )

            text += page_text + "\n"

    except Exception as e:

        print("OCR Error:", e)

        return ""

    print("✅ OCR Completed")
    print("Characters:", len(text))

    return text.strip()