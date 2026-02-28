import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    
    # Replace special characters with space (IMPORTANT CHANGE)
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text