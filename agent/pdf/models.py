import camelot
import pandas
from django.db import models
from pandas import DataFrame
from PyPDF2 import PdfReader, PdfWriter

from agent.models import Agent
from agent.textraction import read_pdf
from agent.token_classification import parse
from base.models import BaseModel


# Create your models here.
class PDFAgent(BaseModel):
    status = models.IntegerField(default=0)
    pdf_cv_file = models.FileField(upload_to="pdf-cv")
    name = models.TextField(null=True)
    email = models.EmailField(null=True)
    mobile_number = models.TextField(null=True)
    skills = models.JSONField(null=True)
    college_name = models.TextField(null=True)
    degree = models.TextField(null=True)
    designation = models.TextField(null=True)
    experience = models.TextField(null=True)
    company_names = models.JSONField(null=True)
    no_of_pages = models.IntegerField(null=True)
    total_experience = models.IntegerField(null=True)
    raw_data = models.TextField(null=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="pdf_agent")

    def pdf_to_text(self):
        try:
            raw_data = read_pdf(self.pdf_cv_file.path)
            print("data")
            self.raw_data = raw_data.replace("\x00", "\uFFFD")
            self.status = 1
            self.save()
        except Exception as e:
            print(e)

    def initial_resume_data(self):
        try:
            token_data = parse(self.pdf_cv_file.path)
            for key, value in token_data.items():
                self.__setattr__(
                    key,
                    value.replace("\x00", "\uFFFD"),
                )
            self.save()
        except Exception as e:
            print(e)

    def run(self):
        self.pdf_to_text()
        self.initial_resume_data()

    def to_dataframe(self) -> DataFrame:
        pass
        df = DataFrame.from_dict(self)
        return df
