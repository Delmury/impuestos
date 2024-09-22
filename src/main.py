import pytesseract
from PIL import Image
import re
import json
from google.cloud import storage

def process_tax_document(event, context):
    """Cloud Function triggered by a change to a Cloud Storage bucket."""
    file = event
    print(f"Processing file: {file['name']}.")

    bucket_name = file['bucket']
    file_name = file['name']
    
    local_file_name = "/tmp/" + file_name.split('/')[-1]
    download_blob(bucket_name, file_name, local_file_name)
    
    extracted_text = extract_text(local_file_name)
    if extracted_text:
        tax_info = extract_tax_info(extracted_text)
        print(json.dumps(tax_info))
        return json.dumps(tax_info), 200
    else:
        print("Text extraction failed.")
        return "Text extraction failed.", 400

def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def extract_text(image_path):
    try:
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