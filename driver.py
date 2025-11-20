    



import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import json

from pathlib import Path
from lambda_function import lambda_handler

BASE_DIR = Path(__file__).resolve().parent

DEBUG = os.environ.get('DEBUG', True)  

if DEBUG:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")

logger.info(f"env variabls: DEBUG: '{DEBUG}', SAMPLE_VARIABLE:'{os.environ.get('SAMPLE_VARIABLE', 'could not fatch the value')}'")

sample_event = {
    # --- Scheme Details ---
    "scheme_id": 1,
    # "scheme_company": "Reyasat Builders",
    # "scheme_name": "Affordable Housing Scheme",
    "scheme_address": "123 Main Street, Pune",

    # --- Application Reference ---
    "application_number": 123456,
    "application_submission_date": "2025-11-18",

    # --- Applicant Details ---
    "applicant_name": "John Doe",
    "father_or_husband_name": "Robert Doe",
    "dob": "1990-05-12",
    "mobile_number": "9876543210",
    "id_type": "Aadhar",
    "id_number": "1234-5678-9012",
    "pan_number": "ABCDE1234F",

    # --- Address Details ---
    "permanent_address": "456 Residential Area, Pune",
    "permanent_address_pincode": "411001",
    "postal_address": "456 Residential Area, Pune",
    "postal_address_pincode": "411001",

    # --- Income & Category ---
    "annual_income": '3L-6L',
    "plot_category": "LIG",
    "registration_fees": 20000,
    "processing_fees": 500,
    "total_payable_amount": 21500,

    # --- Payment Details ---
    "payment_mode": "DD",
    "payment_status": "Paid",
    "dd_id_or_transaction_id": "DD12345",
    "dd_date_or_transaction_date": "2025-11-15",
    "dd_amount": 21500,
    "payee_account_holder_name": "John Doe",
    "payee_bank_name": "State Bank of India",

    # --- Refund Details ---
    "refund_account_holder": "John Doe",
    "refund_account_number": "987654321012",
    "refund_bank_name": "State Bank of India",
    "refund_bank_ifsc": "SBIN0001234",

    # --- HTML / Templates ---
    # "logo_html": "<img src='logo.png' />",
    # "payment_image_html": "<img src='payment.png' />",
    # "refund_section_html": "<div>Refund details here</div>",

    # --- Footer ---
    "print_date": "2025-11-18"
}

json_string = json.dumps(sample_event)

print(json)
responce = lambda_handler(event = json_string, context=None)
print(responce)



{
    "scheme_id": 1,
    "scheme_company": "Reyasat Builders",
    "scheme_name": "Affordable Housing Scheme",
    "scheme_address": "123 Main Street, Pune",
    "application_number": 123456,
    "application_submission_date": "2025-11-18",
    "applicant_name": "John Doe",
    "father_or_husband_name": "Robert Doe",
    "dob": "1990-05-12",
    "mobile_number": "9876543210",
    "id_type": "Aadhar",
    "id_number": "1234-5678-9012",
    "pan_number": "ABCDE1234F",
    "permanent_address": "456 Residential Area, Pune",
    "permanent_address_pincode": "411001",
    "postal_address": "456 Residential Area, Pune",
    "postal_address_pincode": "411001",
    "annual_income": '3L-6L',
    "plot_category": "LIG",
    "registration_fees": 20000,
    "processing_fees": 500,
    "total_payable_amount": 21500,
    "payment_mode": "DD",
    "payment_status": "Paid",
    "dd_id_or_transaction_id": "DD12345",
    "dd_date_or_transaction_date": "2025-11-15",
    "dd_amount": 21500,
    "payee_account_holder_name": "John Doe",
    "payee_bank_name": "State Bank of India",
    "refund_account_holder": "John Doe",
    "refund_account_number": "987654321012",
    "refund_bank_name": "State Bank of India",
    "refund_bank_ifsc": "SBIN0001234",
    "print_date": "2025-11-18"
}



