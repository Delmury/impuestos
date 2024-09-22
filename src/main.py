def process_tax_document(event, context):
    """Cloud Function triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
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

# Keep the rest of the file as is