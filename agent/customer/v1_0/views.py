from io import StringIO

import pandas as pd
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from agent.models import Agent
from agent.pdf.models import PDFAgent
from agent.tasks import run_batch, run_extract_table
from base.pagination import ItemIndexPagination
from agent.pdf_table.models import PdfTable
from .serializers import AgentSerializer, RetrieveAgentSerializer, UploadPdfSerializer


class ListCreateAPIView(ListCreateAPIView):
    pagination_class = ItemIndexPagination
    serializer_class = UploadPdfSerializer
    permission_classes = ()
    queryset = Agent.objects.all()
    parser_classes = [
        MultiPartParser,
    ]

    def get_queryset(self):
        return (
            super().get_queryset().prefetch_related("pdf_agent").order_by("-created_at")
        )

    def get(self, request, *args, **kwargs):
        self.serializer_class = AgentSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data["files"] = request.FILES
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            task_type = serializer.validated_data["type"]

            new_agent = Agent.objects.create(type=task_type)
            files = self.request.FILES
            if task_type == "table_extract":
                for item in files:
                    pdf = PDFAgent.objects.create(
                    pdf_cv_file=files.get(item), agent=new_agent
                )
                pdf.save()
                run_extract_table.delay(pdf.id)
                return Response(data=dict(id=new_agent.id))
            for item in files:
                pdf = PDFAgent.objects.create(
                    pdf_cv_file=files.get(item), agent=new_agent
                )
                pdf.save()
                run_batch.delay(pdf.id)
            self.id = new_agent.id
            return Response(data=dict(id=new_agent.id))


class ExportAgentAPIView(RetrieveAPIView):
    serializer_class = RetrieveAgentSerializer
    permission_classes = ()
    lookup_field = "id"
    lookup_url_kwarg = "agent_id"
    queryset = Agent.objects.all()

    def get_queryset(self):
        return super().get_queryset().prefetch_related("pdf_agent")

    def get(self, request, agent_id, *args, **kwargs):
        return self.export_to_xlsx(agent_id)

    def export_to_xlsx(self, id):
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
