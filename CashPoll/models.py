from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

# Open Poll - Anybody can vote and see the Poll's Progress.

class CashPoll(models.Model):
    unique_id = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return str(self.title)

class CashPollOption(models.Model):
    poll = models.ForeignKey(CashPoll, on_delete=models.CASCADE, related_name="CashPollOptions")
    name = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)