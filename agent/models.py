from django.contrib.auth.models import User
from django.db import models
from base.models import BaseModel
# Create your models here.


class Agent(BaseModel):
    type = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    