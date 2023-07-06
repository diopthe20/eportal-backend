from django.db import models

# Create your models here.

class Agent(models.Model):
    name = models.CharField(max_length=250, null= True)
    batches = models.JSONField()