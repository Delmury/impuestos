if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        local_file_name = sys.argv[1]
        extracted_text = extract_text(local_file_name)
        if extracted_text:
            tax_info = extract_tax_info(extracted_text)
            print(json.dumps(tax_info, indent=2))
        else:
            print("Text extraction failed.")
    else:
        print("Please provide a file path as an argument.")