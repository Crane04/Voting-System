from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class SpecialPoll(models.Model):
    unique_id = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    description = models.TextField()
    voters = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.title)

# Voters Info on a particular Special Poll
class SpecialPollVoters(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    time_requested = models.DateTimeField(default = datetime.now())
    special_poll = models.ForeignKey(SpecialPoll, on_delete=models.CASCADE)
    allowed = models.BooleanField(default = False)
    voted = models.BooleanField(default = False)

    def __str__(self):
        return str(self.special_poll)

# Contestants
class SpecialPollContestants(models.Model):
    poll = models.ForeignKey(SpecialPoll, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)
    option_image = models.ImageField(upload_to="special/option", default = "")

    def __str__(self):
        return str(self.name)