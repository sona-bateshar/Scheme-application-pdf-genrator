import os
from s3_file_uploader import S3FileUploader
# from test_file import generate_acknowledgement_pdf

from clients import clients

class application_pdf_generator:
    def __init__(self, event):
        self.event = event
        self.client = clients.get(self.event.get('client_name', 'null_client'), None)

    def create_pdf(self):

        pdf_content = self.client.pdf_function(self.event) if self.client else "client not found"
        ext = '.pdf'
        scheme_id = self.event.get('scheme_id', 'null_scheme')
        scheme_name = self.event.get('scheme_name', 'null_scheme')
        application_number  = self.event.get('application_number', 'null_application_number')

        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        # AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

        AWS_STORAGE_BUCKET_NAME = self.client.s3_bucket

        # print(AWS_STORAGE_BUCKET_NAME)
        AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', "ap-south-1")

        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

        # write in s3
        file_path = f"applications/{scheme_id}/acknowledge_pdfs/Acknowledgement_{scheme_id}_{application_number}{ext}"

        if os.environ.get('DEBUG', 'True') == 'False':
            uploader = S3FileUploader(AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME , AWS_ACCESS_KEY_ID,  AWS_SECRET_ACCESS_KEY)
            result = uploader.upload_file(
                file_content=pdf_content,
                file_path=file_path,
                content_type='application/pdf', 
                metadata={'uploaded_by': 'lambda_function'}
            )
        else:
            # write in local for testing
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test/output.pdf"), "wb") as f:
                f.write(pdf_content)
            result = None
        
        
        return {
            'statusCode': 200 if result and result.get('success') else 500,
            'body': result
        }