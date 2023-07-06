import pdfminer
from pdfminer.high_level import extract_text


def read_pdf(file):
    text = extract_text(file)
    return text

 