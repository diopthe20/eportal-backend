from rest_framework import serializers

from ...models import Converter
from ...tasks import convert_pdf_to_docx


class ConvertSerializer(serializers.ModelSerializer):
    original_file = serializers.FileField()

    class Meta:
        model = Converter
        fields = [
            "id",
            "status",
            "created_at",
            "modified_at",
            "original_thumbnail",
            "original_file",
            "converted_file",
        ]

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        convert_pdf_to_docx.delay(convert_id=instance.id)
        return instance
