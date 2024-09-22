import pytesseract
from PIL import Image
import re
import json
from google.cloud import storage

def load_config():
    # In a cloud environment, you might want to use environment variables
    # or secret management instead of a config file
    import os
    return {
        "tesseract_path": os.environ.get("TESSERACT_PATH", "/usr/bin/tesseract"),
        "output_format": os.environ.get("OUTPUT_FORMAT", "json")
    }

def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def extract_text(image_path):
    try:
        config = load_config()
        pytesseract.pytesseract.tesseract_cmd = config['tesseract_path']
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def extract_tax_info(text):
    # This is a simple example. You'd need to adjust these patterns for actual tax documents.
    tax_id_pattern = r'Tax ID: (\d{9})'
    income_pattern = r'Total Income: \$(\d+(\.\d{2})?)'
    
    tax_id = re.search(tax_id_pattern, text)
    income = re.search(income_pattern, text)
    
    return {
        'tax_id': tax_id.group(1) if tax_id else None,
        'income': income.group(1) if income else None
    }

def process_tax_document(request):
    # This function would be your Cloud Function or Cloud Run entry point
    if request.method != 'POST':
        return 'Send a POST request', 405
    
    content = request.get_json()
    bucket_name = content['bucket']
    file_name = content['name']
    
    local_file_name = "/tmp/" + file_name.split('/')[-1]
    download_blob(bucket_name, file_name, local_file_name)
    
    extracted_text = extract_text(local_file_name)
    if extracted_text:
        tax_info = extract_tax_info(extracted_text)
        return json.dumps(tax_info), 200
    else:
        return "Text extraction failed.", 400

# The __main__ block is not needed for Cloud Functions or Cloud Run