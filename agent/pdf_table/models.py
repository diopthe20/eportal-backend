import camelot
import pandas
from django.db import models
from PyPDF2 import PdfReader, PdfWriter

from base.models import BaseModel


class PdfTable(BaseModel):
    status = models.IntegerField(default=0)
    pdf_cv_file = models.FileField(upload_to="pdf-cv")
    data = models.JSONField(null=True)

    def read_table_from_pdf(self):
        inputpdf = PdfReader(open(self.pdf_cv_file.path, "rb"))
        arr = []
        for i in range(len(inputpdf.pages)):
            output = PdfWriter()
            output.add_page(inputpdf.pages[i])
            arr.append("temp/document-page%s.pdf" % i)
            with open("temp/document-page%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)
        results = []
        for i in arr:
            tables = camelot.read_pdf(i)
            results.append(tables)
        rl = [i[0].df[1:] for i in results]
        rl = pandas.concat(rl, ignore_index=True)
        self.data = rl.to_dict()
        self.save()
