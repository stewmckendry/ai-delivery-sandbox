import os
import html
import docx
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".pdf":
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                return "\n".join(page.extract_text() or "" for page in reader.pages)

        elif ext == ".docx":
            doc = docx.Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs)

        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        elif ext in [".html", ".htm"]:
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                return soup.get_text()

        else:
            return f"[Unsupported file type: {ext}]"

    except Exception as e:
        return f"[ERROR parsing {file_path}]: {str(e)}"