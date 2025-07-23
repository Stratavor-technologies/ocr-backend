from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

def extract_xfa_xml(pdf_path):
    document = fitz.open(pdf_path)
    xfa_xml = None

    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        for widget in page.widgets():
            if widget.field_type == fitz.PDF_WIDGET_TYPE_TEXT:
                # Access XFA XML data here (if available)
                xfa_xml = widget.field_value  # This is illustrative; actual extraction will vary

    return xfa_xml

# Example usage
pdf_file_path = r'C:\Users\anjal\Downloads\BOIR.pdf'
extracted_text = extract_xfa_xml(pdf_file_path)
print("Extracted Text: ", extracted_text)