$content = @"
import pytesseract
from PIL import Image
import re
import json

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

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

if __name__ == "__main__":
    config = load_config()
    image_path = "path/to/your/tax_document.jpg"
    extracted_text = extract_text(image_path)
    if extracted_text:
        tax_info = extract_tax_info(extracted_text)
        print("Extracted tax information:")
        print(json.dumps(tax_info, indent=2))
    else:
        print("Text extraction failed.")
"@

Set-Content -Path src\ocr_app.py -Value $content