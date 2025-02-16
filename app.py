from flask import Flask, request, jsonify, abort
from typing import List
import os
from dotenv import load_dotenv
from Services.csv_service import get_payroll_data_from_csv
from Services.email_service import send_email
from Services.pdf_service import generate_pdf
from datetime import datetime


load_dotenv()
app = Flask(__name__)

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')

@app.route('/process',methods=['POST'])
def process_payroll():

    auth = request.args.get('credentials','').split(' ')
    if len(auth) != 2 or auth[0] != API_USER or auth[1] != API_PASSWORD:
        abort(401,"Invalid Credentials")


    country = request.args.get('country','do')
    company = request.args.get('company')
    if not company:
        abort(400, "Company parameter is required")

    country = request.args.get("country", "do")
    company = request.args.get("company")
    if not company:
        abort(400, "Company parameter is required")

    if len(request.files) == 0:
        abort(400, "File parameter is required")

    if len(request.files) > 1:
        abort(400, "Only one file is allowed")

    csv_file = None
    for file_key in request.files:
        csv_file = request.files[file_key]
        break

    if not csv_file.filename.endswith(".csv"):
        abort(400, "Only CSV files are allowed")

    if csv_file.content_type != "text/csv":
        abort(400, "Invalid file type. Only CSV files are allowed")

    payroll_emails_succesfully_send= []
    try:
        client_data = get_payroll_data_from_csv(csv_file, country)
        for client in client_data:
            if client.email:
                pdf = generate_pdf(client, country, company)
                send_email(client, country, pdf)
                client.read_date = datetime.now()
                payroll_emails_succesfully_send.append(client.to_dict())
    except ValueError as e:
        abort(400, str(e))

    return jsonify({"status": "success", "clients": payroll_emails_succesfully_send})

if __name__ == "__main__":
    app.run()