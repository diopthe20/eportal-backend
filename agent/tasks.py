from celery import shared_task

from agent.pdf.models import PDFAgent
from agent.pdf_table.models import PdfTable


@shared_task
def run_batch(pdf_id):
    print(pdf_id)
    pdf = PDFAgent.objects.get(id=pdf_id)
    pdf.run()
    pdf.status = 2
    pdf.save()
    return "completed"


@shared_task
def run_extract_table(pdf_id):
    print(pdf_id)
    pdf = PdfTable.objects.get(id=pdf_id)
    pdf.read_table_from_pdf()
    pdf.status = 2
    pdf.save()
    return "completed"
