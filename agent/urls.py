from django.contrib import admin
from django.urls import path

from agent.views import (
    FileFieldFormView,
    agent_detail_view,
    export_to_xlsx,
    task_status,
    task_view,
)

urlpatterns = [
    path("upload/", FileFieldFormView.as_view()),
    path("<int:id>", agent_detail_view),
    path("<int:id>/export", export_to_xlsx),
    path("", task_view),
    path("<int:agent_id>/status/", task_status),
]
