
import re
from datetime import datetime


class EventValidator:
    def __init__(self, event):
        self.event = event

    # Generic string validator
    def validate_string(self, value, field_name, max_length=255, allow_spaces=True):
        """
        Validates a string field.
        - max_length: maximum allowed length
        - allow_spaces: whether spaces are allowed
        - prevents basic injection by allowing only safe characters
        """
        if value is None:
            raise ValueError(f"Field '{field_name}' cannot be null")
        
        if not isinstance(value, str):
            raise ValueError(f"Field '{field_name}' must be a string")
        
        if len(value) > max_length:
            raise ValueError(f"Field '{field_name}' exceeds max length of {max_length}")
        
        # Allow only letters, numbers, basic punctuation, and optionally spaces
        pattern = r'^[a-zA-Z0-9@.,&()\-/_]*$' if not allow_spaces else r'^[a-zA-Z0-9 @.,&()\-/_]*$'
        
        if not re.match(pattern, value):
            raise ValueError(f"Field '{field_name}' contains invalid characters")
        
        return value.strip()

    
    def validate_number(self, value, field_name, min_value=-10**9, max_value=10**9):
        """
        Validates numeric fields like amounts or IDs.
        """
        if value is None:
            raise ValueError(f"Field '{field_name}' cannot be null")
        
        if not isinstance(value, (int, float)):
            raise ValueError(f"Field '{field_name}' must be a number")
        
        if min_value is not None and value < min_value:
            raise ValueError(f"Field '{field_name}' cannot be less than {min_value}")
        
        if max_value is not None and value > max_value:
            raise ValueError(f"Field '{field_name}' cannot exceed {max_value}")
        
        return value

    def validate_date(self, value, field_name, date_format="%Y-%m-%d"):
        """
        Validates date fields.
        """
        if value is None:
            raise ValueError(f"Field '{field_name}' cannot be null")
        
        if isinstance(value, str):
            try:
                dt = datetime.strptime(value, date_format)
            except ValueError:
                raise ValueError(f"Field '{field_name}' must be a valid date in format {date_format}")
            return dt
        elif isinstance(value, datetime):
            return value
        else:
            raise ValueError(f"Field '{field_name}' must be a string or datetime object")
    
    def validate_event(self):
        event  = self.event
        # Scheme details
        self.validate_number(event.get('scheme_id'), 'scheme_id')
        self.validate_string(event.get('scheme_company'), 'scheme_company')
        self.validate_string(event.get('scheme_name'), 'scheme_name')
        self.validate_string(event.get('scheme_address'), 'scheme_address')
        
        # Application Reference
        self.validate_number(event.get('application_number'), 'application_number')
        self.validate_date(event.get('application_submission_date'), 'application_submission_date')
        
        # Applicant Details
        self.validate_string(event.get('applicant_name'), 'applicant_name')
        self.validate_string(event.get('father_or_husband_name'), 'father_or_husband_name')
        self.validate_date(event.get('dob'), 'dob')
        self.validate_string(event.get('mobile_number'), 'mobile_number')
        self.validate_string(event.get('id_type'), 'id_type')
        self.validate_string(event.get('id_number'), 'id_number')
        self.validate_string(event.get('pan_number'), 'pan_number')
        
        # Address Details
        self.validate_string(event.get('permanent_address'), 'permanent_address')
        self.validate_string(event.get('permanent_address_pincode'), 'permanent_address_pincode')
        self.validate_string(event.get('postal_address'), 'postal_address')
        self.validate_string(event.get('postal_address_pincode'), 'postal_address_pincode')
        
        # Income & Category
        self.validate_string(event.get('annual_income'), 'annual_income')
        self.validate_string(event.get('plot_category'), 'plot_category')
        self.validate_number(event.get('registration_fees'), 'registration_fees', 0)
        self.validate_number(event.get('processing_fees'), 'processing_fees', 0)
        self.validate_number(event.get('total_payable_amount'), 'total_payable_amount', 0)
        
        # Payment Details
        self.validate_string(event.get('payment_mode'), 'payment_mode')
        self.validate_string(event.get('payment_status'), 'payment_status')
        self.validate_string(event.get('dd_id_or_transaction_id'), 'dd_id_or_transaction_id')
        self.validate_date(event.get('dd_date_or_transaction_date'), 'dd_date_or_transaction_date')
        self.validate_number(event.get('dd_amount'), 'dd_amount', 0)
        self.validate_string(event.get('payee_account_holder_name'), 'payee_account_holder_name')
        self.validate_string(event.get('payee_bank_name'), 'payee_bank_name')

        # --- Refund Details ---
        self.validate_string(event.get('refund_account_holder'), 'refund_account_holder')
        self.validate_string(event.get('refund_account_number'), 'refund_account_number')
        self.validate_string(event.get('refund_bank_name'), 'refund_bank_name')
        self.validate_string(event.get('refund_bank_ifsc'), 'refund_bank_ifsc')
        
        # # --- HTML fields (optional sanitization) ---
        # self.validate_string(event.get('logo_html', ''), 'logo_html', max_length=5000)
        # self.validate_string(event.get('payment_image_html', ''), 'payment_image_html', max_length=5000)
        # self.validate_string(event.get('refund_section_html', ''), 'refund_section_html', max_length=5000)
        
        # --- Footer ---
        self.validate_string(event.get('print_date'), 'print_date')
        
        return True
