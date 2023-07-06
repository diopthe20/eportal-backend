from django.contrib import admin
from django.urls import path

from agent.views import FileFieldFormView

urlpatterns = [
    path("upload/", FileFieldFormView.as_view()),
]
