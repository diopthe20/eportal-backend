import camelot
import pandas
from django.db import models
from PyPDF2 import PdfReader, PdfWriter

from agent.models import Agent
from base.models import BaseModel


class PdfTable(BaseModel):
    status = models.IntegerField(default=0)
    pdf_cv_file = models.FileField(upload_to="pdf-cv")
    data = models.JSONField(null=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="pdf_table")

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
        rl = []
        for i in results:
            if len(i) == 0:
                continue
            else:
                for item in i:
                    rl.append(item.df[:])

        rl = pandas.concat(rl, ignore_index=True)
        rl = rl.where(pandas.notnull(rl), None)

        self.data = rl.to_dict(orient="records")
        self.save()


"""
[2023-07-12 19:43:13,913: ERROR/MainProcess] Task agent.tasks.run_extract_table[3307def2-297f-4c53-bbb7-a34435588414] raised unexpected: IndexError('list index out of range')
Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/celery/app/trace.py", line 477, in trace_task
    R = retval = fun(*args, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/celery/app/trace.py", line 760, in __protected_call__
    return self.run(*args, **kwargs)
  File "/code/agent/tasks.py", line 21, in run_extract_table
    pdf.read_table_from_pdf()
  File "/code/agent/pdf_table/models.py", line 29, in read_table_from_pdf
    rl = [i[0].df[1:] for i in results]
  File "/code/agent/pdf_table/models.py", line 29, in <listcomp>
    rl = [i[0].df[1:] for i in results]
  File "/usr/local/lib/python3.9/site-packages/camelot/core.py", line 689, in __getitem__
    return self._tables[idx]
IndexError: list index out of range

"""
