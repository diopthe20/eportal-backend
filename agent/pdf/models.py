from django.db import models
from pandas import DataFrame

from agent.textraction import read_pdf
from agent.token_classification import parse


# Create your models here.
class PDFAgent(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.IntegerField(default=0)
    pdf_cv_file = models.FileField(upload_to="pdf-cv")
    name = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(null=True)
    mobile_number = models.CharField(max_length=100, null=True)
    skills = models.JSONField(null=True)
    college_name = models.CharField(max_length=250, null=True)
    degree = models.CharField(max_length=250, null=True)
    designation = models.CharField(max_length=250, null=True)
    experience = models.CharField(max_length=250, null=True)
    company_names = models.JSONField(null=True)
    no_of_pages = models.IntegerField(null=True)
    total_experience = models.IntegerField(null=True)
    raw_data = models.TextField(null=True)

    def pdf_to_text(self):
        raw_data = read_pdf(self.pdf_cv_file.path)
        print("data")
        self.raw_data = raw_data
        self.status = 1
        self.save()

    def initial_resume_data(self):
        token_data = parse(self.pdf_cv_file.path)
        for key, value in token_data.items():
            self.__setattr__(key, value)
        self.status = 2
        self.save()

    def run(self):
        self.pdf_to_text()
        self.initial_resume_data()

    def to_dataframe(self) -> DataFrame:
        pass
        df = DataFrame.from_dict(self)
        return df
