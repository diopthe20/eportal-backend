import os

import fitz
from django.core.files.base import ContentFile, File
from django.db import models
from pdf2docx import Converter as cvt

from base.models import BaseModel


class Converter(BaseModel):
    original_file = models.FileField(upload_to="data")
    status = models.IntegerField(default=0)
    original_thumbnail = models.FileField(upload_to="data", null=True)
    converted_file = models.FileField(upload_to="data", null=True)

    def process(self):
        """
        Stage 1: Preparing
        """
        pdf_file = self.original_file.name
        file_name = os.path.basename(pdf_file)
        file_name.replace(".pdf", "")
        print(pdf_file)
        self.status = 1

        self.get_thumbnail(file_name)
        self.save()
        """
        Stage 2: Converting
        """
        converted = f"media/data/{file_name}.docx"
        cv = cvt(f"{self.original_file.path}")
        cv.convert(converted)
        cv.close()

        converted = f"data/{file_name}.docx"

        self.converted_file = converted

        self.status = 2
        self.save()

    def get_thumbnail(self, file_base_name):
        pdf = fitz.open(f"{self.original_file.path}")
        page = pdf[0]
        image = page.get_pixmap()
        thumnail = f"media/data/{file_base_name}.png"
        image.save(thumnail)

        thumnail = f"data/{file_base_name}.png"
        self.original_thumbnail = thumnail
