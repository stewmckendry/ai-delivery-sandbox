import textract
import docx
import os
import html
from bs4 import BeautifulSoup

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".pdf" or ext == ".docx" or ext == ".pptx":
            return textract.process(file_path).decode("utf-8")
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif ext == ".html" or ext == ".htm":
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                return soup.get_text()
        else:
            return textract.process(file_path).decode("utf-8")
    except Exception as e:
        return f"[ERROR parsing {file_path}]: {str(e)}"