from pdfminer.high_level import extract_text
import docx

def extract_text_from_pdf(filepath):
    """Extracts text from a PDF file."""
    try:
        text = extract_text(filepath)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(filepath):
    """Extracts text from a DOCX file."""
    try:
        doc = docx.Document(filepath)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""
