from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_path

class LocalOCREngine:
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        # First, attempt native digital PDF text extraction
        reader = PdfReader(pdf_path)
        extracted_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            extracted_text += f"--- Page {i+1} ---\n" + text + "\n"

        # Fallback to OCR only if no selectable text was found
        if len(extracted_text.strip()) < 50:
            images = convert_from_path(pdf_path)
            ocr_text = []
            for i, image in enumerate(images):
                ocr_text.append(f"--- Page {i+1} ---\n" + pytesseract.image_to_string(image))
            extracted_text = "\n\n".join(ocr_text)

        return extracted_text
