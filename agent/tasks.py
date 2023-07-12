from celery import shared_task

from agent.models import Agent
from agent.pdf.models import PDFAgent
from agent.pdf_table.models import PdfTable


@shared_task
def run_batch(array, agent_id):
    agent = Agent.objects.get(id=agent_id)
    agent.status = 1
    agent.save()
    for pdf_id in array:
        print(pdf_id)
        pdf = PDFAgent.objects.get(id=pdf_id)
        pdf.run()
        pdf.status = 2
        pdf.save()
    agent.status = 2
    agent.save()
    return "completed"


@shared_task
def run_extract_table(pdf_id):
    print(pdf_id)
    pdf = PdfTable.objects.get(id=pdf_id)
    pdf.agent.status = 1
    pdf.agent.save()
    pdf.read_table_from_pdf()
    pdf.status = 2
    pdf.save()
    pdf.agent.status = 2
    pdf.agent.save()
    return "completed"
