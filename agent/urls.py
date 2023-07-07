from django.contrib import admin
from django.urls import path

from agent.views import FileFieldFormView, agent_detail_view, task_view, export_to_xlsx

urlpatterns = [
    path("upload/", FileFieldFormView.as_view()),
    path("<int:id>", agent_detail_view),
    path("<int:id>/export", export_to_xlsx),
    path("", task_view),
]
