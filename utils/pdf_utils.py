import fitz  # PyMuPDF
import PyPDF2
import json
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, TextStringObject
from io import BytesIO

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_field_info(fields):
    extracted_info = []
    key=0
    for field_name, attributes in fields.items():
        field_info = {
            'Name': attributes.get('/T', field_name),
            'Type': attributes.get('/FT', 'Unknown'),
            'Parent': attributes.get('/Parent', {}).get('/T', 'None'),
            'Flags': attributes.get('/Ff', 'None'),
            'Value': attributes.get('/V', 'None')
        }
        key += 1
        extracted_info.append(field_info)
    # return extracted_info
    return json.dumps(extracted_info, indent=4)


def extract_form_fields(file_path):
    fields = []
    with fitz.open(file_path) as doc:
        for page in doc:
            for field in page.widgets():

                if field.field_name:
                    fieldname = field.field_name.split(".")[-1]
                else:
                    fieldname = ""

                field_info = {
                    'Name': fieldname,
                    'Type': field.field_type,
                    'Value': field.field_value
                }
                fields.append(field_info)
    return json.dumps(fields, indent=4)


def update_pdf_form_fields(file_path, field_updates):
    reader = PdfReader(file_path)
    writer = PdfWriter()

    if reader.is_encrypted:
        reader.decrypt('')

    # Update form fields
    for page_num, page in enumerate(reader.pages):
        if '/Annots' in page:
            for annot in page['/Annots']:
                field_object = annot.get_object()
                field_name = field_object.get('/T')
                if field_name and field_name in field_updates:
                    field_object.update({
                        NameObject('/V'): TextStringObject(field_updates[field_name])
                    })
        
        # Add updated page to writer
        writer.add_page(page)

    # Write the updated PDF to the output file
    # with open(output_path, 'wb') as output_file:
    #     writer.write(output_file)

    pdf_bytes = BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)

    return pdf_bytes