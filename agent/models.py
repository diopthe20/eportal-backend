from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Agent(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)