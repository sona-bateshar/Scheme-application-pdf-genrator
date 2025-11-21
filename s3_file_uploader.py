import boto3
import os
import logging
from botocore.exceptions import ClientError
from typing import Optional, Union, BinaryIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class S3FileUploader:
    """
    Utility class for handling file uploads to S3 bucket.
    Checks if file exists and overwrites or creates new file accordingly.
    """
    def __init__(
        self, 
        bucket_name: str, 
        region: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None
    ):
        """
        Initialize S3 uploader with bucket name and optional AWS credentials.
        Automatically works with Lambda's IAM role if credentials are not provided.
        """
        self.bucket_name = bucket_name

        if os.environ.get('DEBUG', 'True').lower() == 'true':
            # Local mode: use provided credentials
            self.s3_client = boto3.client(
                's3',
                region_name=region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token
            )
        else:
            # Lambda / AWS mode: use IAM role
            self.s3_client = boto3.client('s3', region_name=region)
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists in the S3 bucket.
        
        Args:
            file_path: The S3 object key (file path)
            
        Returns:
            True if file exists, False otherwise
        """
        
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_path)
            logger.info(f"File '{file_path}' exists in bucket '{self.bucket_name}'")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.info(f"File '{file_path}' does not exist in bucket '{self.bucket_name}'")
                return False
            else:
                logger.error(f"Error checking file existence: {str(e)}")
                return False
        except:
            return False
    
    def upload_file(
        self, 
        file_content: Union[bytes, str, BinaryIO], 
        file_path: str,
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> dict:
        """
        Upload file to S3 bucket. Overwrites if file exists, creates new otherwise.
        
        Args:
            file_content: File content as bytes, string, or file object
            file_path: The S3 object key (destination path)
            content_type: MIME type of the file (optional)
            metadata: Additional metadata for the file (optional)
            
        Returns:
            Dictionary with upload status and details
        """
        # print("file_content:", file_content[:20], type(file_content))

        try:
            
            # Check if file exists
            # exists = self.file_exists(file_path)
            
            # Prepare upload parameters
            upload_params = {
                'Bucket': self.bucket_name,
                'Key': file_path,
                'Body': file_content
            }
            
            if content_type:
                upload_params['ContentType'] = content_type
            
            if metadata:
                upload_params['Metadata'] = metadata
            
            # Upload file
            response = self.s3_client.put_object(**upload_params)
            # action = "overwritten" if exists else "created"
            logger.info(f"File '{file_path}' successfully in bucket '{self.bucket_name}'")
            
            return {
                'success': True,
                # 'action': action,
                'file_key': file_path,
                'bucket': self.bucket_name,
                'version_id': response.get('VersionId'),
                'etag': response.get('ETag')
            }
            
        except ClientError as e:
            logger.error(f"Error uploading file: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'file_key': file_path,
                'bucket': self.bucket_name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_key': file_path,
                'bucket': self.bucket_name
            }
    