from celery import shared_task

from agent.pdf.models import PDFAgent


@shared_task
def run_batch(pdf_id):
    print(pdf_id)
    pdf = PDFAgent.objects.get(id=pdf_id)
    pdf.run()
    pdf.status = 2
    pdf.save()
    return "completed"
