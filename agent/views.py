import json
from io import StringIO

import pandas as pd
import xlsxwriter
from django.core import serializers
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.db import models
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView

from agent.pdf.models import PDFAgent

from .forms import FileFieldForm
from .models import Agent
from .tasks import run_batch


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "agent/upload.html"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_agent = Agent.objects.create()
        files = self.request.FILES
        for item in files:
            pdf = PDFAgent.objects.create(pdf_cv_file=files.get(item), agent=new_agent)
            pdf.save()
            run_batch.delay(pdf.id)
        self.id = new_agent.id
        return JsonResponse(data=dict(id=new_agent.id))

    def form_invalid(self, form):
        return HttpResponseBadRequest()


def agent_detail_view(request, id):
    context = {}
    queryset = PDFAgent.objects.filter(agent_id=id)
    context["data"] = queryset
    return render(request, "agent/detail_view.html", context)


def task_view(request):
    '''
    Docstring
    ## Hello
    - List 1
    - List 2
    '''
    context = {}
    queryset = Agent.objects.all().prefetch_related("pdf_agent")
    pdf_task = PDFAgent.objects.all()
    for item in queryset:
        pdfs = pdf_task.filter(agent_id=item.id).values("status")
        item.total = len(pdfs)
        if item.total == 0:
            item.status = 0
            continue
        completed = pdf_task.filter(agent_id=item.id, status=2)
        item.status = int(len(completed) / len(pdfs) * 100)

    context["data"] = queryset
    return render(request, "agent/task_view.html", context)


def task_status(request, agent_id):
    all_tasks = PDFAgent.objects.filter(agent_id=agent_id)
    completed = all_tasks.filter(status=2)
    status = int(len(completed) / len(all_tasks) * 100)
    return JsonResponse(data=dict(status=status))


def export_to_xlsx(request, id):
    queryset = PDFAgent.objects.filter(agent_id=id)
    fields = [
        "pdf_cv_file",
        "name",
        "email",
        "mobile_number",
        "skills",
        "college_name",
        "degree",
        "designation",
        "experience",
        "company_names",
        "total_experience",
        "raw_data",
    ]
    data = []
    for item in queryset:
        new_item = {}
        for field in fields:
            if type(item.__getattribute__(field)) == list:
                item.__setattr__(field, " ".join(item.__getattribute__(field)))
                new_item[field] = item.__getattribute__(field)
            elif field == "pdf_cv_file":
                new_item[field] = item.__getattribute__(field).name
            else:
                new_item[field] = item.__getattribute__(field)
        data.append(new_item)

    output = StringIO()
    df = pd.DataFrame.from_dict(data)
    df.to_excel(f"output/{id}.xlsx")
    # create a response
    file_name = f"output/{id}.xlsx"
    with open(file_name, "rb") as f:
        file_data = f.read()
    response = HttpResponse(
        file_data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f"attachment; filename={file_name}"
    return response
