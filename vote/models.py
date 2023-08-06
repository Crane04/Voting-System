from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Poll(models.Model):
    unique_id = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    def __str__(self):
        return str(self.title)

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)