# Tax Document OCR Project

This project uses OCR (Optical Character Recognition) to extract information from tax documents using Google Cloud services.

## Setup
1. Install requirements: `pip install -r src/requirements.txt`
2. Set up Google Cloud credentials
3. Deploy to Google Cloud Functions

## Deployment
Deploy the function using:
```
gcloud functions deploy process_tax_document --runtime python39 --trigger-resource generative-ai-436415-tax-documents --trigger-event google.storage.object.finalize --entry-point process_tax_document --source src --region us