from celery import shared_task
from .models import Converter



@shared_task
def convert_pdf_to_docx(convert_id):
    task = Converter.objects.get(id=convert_id)
    task.process()
    return "completed"