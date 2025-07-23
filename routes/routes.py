from flask import Blueprint, request, jsonify, current_app, make_response, send_file
import os
from werkzeug.utils import secure_filename
from ..utils.pdf_utils import extract_text_from_pdf, extract_form_fields, update_pdf_form_fields, extract_field_info
import json


# Define a Blueprint
bp = Blueprint('main', __name__)

@bp.route("/", methods=['GET'])
def home():
    return "Hello, Welcome to the ORC Application homepage"


@bp.route("/upload", methods=['POST'])
def upload_file():
    files = request.files.getlist('pdfFile')
    # if 'pdfFile' not in request.files:
    #     return jsonify({'error': 'No file part'})
    pdfsData = []
    for file in files:

    # file = request.files['pdfFile']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            

            # Define the updates to apply to form fields
            # updates = {
            #     'ReportingCompanyName[0]': 'Anmol Batti Updated Name',
            #     'CompanyIDNumber[0]': '123456'
            # }

            # updated_file_path = os.path.join(upload_folder, "updated_pdf.pdf")
            # update_pdf_form_fields(file_path, updated_file_path, updates)

            # Extract text and form fields from the updated PDF
            text = extract_text_from_pdf(file_path)
            form_fields = extract_form_fields(file_path)

            pdfsData.append({
                'text': text,
                'form_fields': form_fields,
                'file_path': file_path,
                'filename': filename
            })

        else:
            return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'})

    # print("pdfsData: ", pdfsData)
    return jsonify({
        "pdfsData": pdfsData
    })



@bp.route("/update-pdf", methods=['POST'])
def update_pdf():
    data = request.get_json()

    # file_path = data.get('file_path')
    updates = data.get('updatedFields')

    # part1UpdatedSeparatedAdd = updates['partner_address[0]'].split(",")
    # # part2UpdatedSeparatedAdd = updates['company_current_address_seperated[0]'].split(",")
    # part3UpdatedSeparatedAdd = updates['partner_address[0]'].split(",")

    # boirUpdated = {
    #     "ReportingCompanyLegalName[0]": updates['partner_name[0]'],
    #     "partner_address[0]": updates['partner_address[0]'],
    #     "tax_id_number[0]": updates['partner_pssn_tin[0]'],
    #     "part_3_legal_name[0]": updates['partner_name[0]'],
    #     "part_3_address_full[0]": updates['partner_address[0]'],
    #     # "part2_current_address[0]": updates['company_current_address[0]'],

    #     # "part2_city[0]": part2UpdatedSeparatedAdd[0],
    #     # "part2_state[0]": part2UpdatedSeparatedAdd[1],
    #     # "part2_zipcode[0]": part2UpdatedSeparatedAdd[2],

    #     "part1_city[0]": part1UpdatedSeparatedAdd[0],
    #     "part1_state[0]": part1UpdatedSeparatedAdd[1],
    #     "part1_zipcode[0]": part1UpdatedSeparatedAdd[2],

    #     "part_3_resi_city[0]": part3UpdatedSeparatedAdd[0],
    #     "part_3_resi_state[0]": part3UpdatedSeparatedAdd[1],
    #     "part_3_resi_zipcode[0]": part3UpdatedSeparatedAdd[2],

    # }
    partner_address = updates.get('partner_address[0]', '')
    part1UpdatedSeparatedAdd = partner_address.split(",")
    part3UpdatedSeparatedAdd = partner_address.split(",")

    boirUpdated = {
        "ReportingCompanyLegalName[0]": updates.get('partner_name[0]', ''),
        "partner_address[0]": partner_address,
        "tax_id_number[0]": updates.get('partner_pssn_tin[0]', ''),
        "part_3_legal_name[0]": updates.get('partner_name[0]', ''),
        "part_3_address_full[0]": updates.get('partner_address[0]', ''),
        
        "part1_city[0]": part1UpdatedSeparatedAdd[0] if len(part1UpdatedSeparatedAdd) > 0 else '',
        "part1_state[0]": part1UpdatedSeparatedAdd[1] if len(part1UpdatedSeparatedAdd) > 1 else '',
        "part1_zipcode[0]": part1UpdatedSeparatedAdd[2] if len(part1UpdatedSeparatedAdd) > 2 else '',

        "part_3_resi_city[0]": part3UpdatedSeparatedAdd[0] if len(part3UpdatedSeparatedAdd) > 0 else '',
        "part_3_resi_state[0]": part3UpdatedSeparatedAdd[1] if len(part3UpdatedSeparatedAdd) > 1 else '',
        "part_3_resi_zipcode[0]": part3UpdatedSeparatedAdd[2] if len(part3UpdatedSeparatedAdd) > 2 else '',
    }

    updated_pdf = update_pdf_form_fields('BOIR4_static.pdf', boirUpdated)

    response = make_response(updated_pdf.read())
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='BOIR.pdf')

    # return jsonify({
    #     'message': "PDF updated successfully",
    #     # 'file_path': file_path
    # })

    return response