import camelot
from PyPDF2 import PdfWriter, PdfReader
import pandas 

def read_table_from_pdf(filename):
    inputpdf = PdfReader(open(filename, "rb"))
    arr = []
    for i in range(len(inputpdf.pages)):
        output = PdfWriter()
        output.add_page(inputpdf.pages[i])
        arr.append("document-page%s.pdf" % i)
        with open("document-page%s.pdf" % i, "wb") as outputStream:
            output.write(outputStream)
    results = []
    for i in arr: 
        tables = camelot.read_pdf(i)
        results.append(tables)
    rl = [i[0].df[1:] for i in results]
    rl = pandas.concat(rl, ignore_index=True)
    return rl