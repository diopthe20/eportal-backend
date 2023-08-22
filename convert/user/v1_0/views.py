from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ...models import Converter
from .serializers import ConvertSerializer


class ConvertListCreateAPIView(ListCreateAPIView):
    serializer_class = ConvertSerializer
    permission_classes = []
    queryset = Converter.objects.all().order_by("-created_at")


class ConvertRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ConvertSerializer
    permission_classes = []
    queryset = Converter.objects.all().order_by("-created_at")
