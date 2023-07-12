from django.contrib import admin
from django.urls import path

from .views import ExportAgentAPIView, ListCreateAPIView

urlpatterns = [
    path("", ListCreateAPIView.as_view(), name="list-create-agent"),
    path("<uuid:agent_id>/export/", ExportAgentAPIView.as_view(), name="export-agent"),
]
