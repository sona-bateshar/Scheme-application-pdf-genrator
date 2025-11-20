import json
import logging
from verification import EventValidator
from pdf_genrator import application_pdf_generator

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Step 2: Lambda handler
def lambda_handler(event, context):
    try:
        # If the incoming event is a JSON string → parse it
        if isinstance(event, str):
            try:
                event = json.loads(event)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON payload: {e.msg}") from e
            
            
        # Validate the event
        validator = EventValidator(event)
        responce = validator.validate_event()
        logger.info(f"data validation:'{responce if responce is True else False}' ")

        # If validation passes, continue with processing
        try:
            responce = application_pdf_generator(event).create_pdf()
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "internal server error": str(e)
                })
            }
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Event processed successfully",
                                "responce":responce})
        }
    
    except ValueError as e:
        # Catch validation errors and return structured JSON
        error_msg = str(e)
        # Extract the field name from the error message
        # Assuming error message format: "Field 'field_name' ... "
        field_name = error_msg.split("'")[1] if "'" in error_msg else "unknown"
        
        return {
            "statusCode": 400,
            "body": json.dumps({
                "input_error": {
                    field_name: error_msg
                }
            })
        }
