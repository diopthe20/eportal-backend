from django.urls import path

from .views import ConvertListCreateAPIView, ConvertRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("", ConvertListCreateAPIView.as_view(), name="convert-list-create"),
    path(
        "<uuid:pk>/",
        ConvertRetrieveUpdateDestroyAPIView.as_view(),
        name="convert-list-create",
    ),
]
