from django.contrib import admin
from .models import *
# Register your models here.

class PollAdmin(admin.ModelAdmin):
    list_display = ("title","admin", "time_start", "time_end")

class OptionAdmin(admin.ModelAdmin):
    list_display = ("poll", "name", "votes")

class VoterAdmin(admin.ModelAdmin):
    list_display = ("poll", "user")

class SpecialPollAdmin(admin.ModelAdmin):
    list_display = ("title","admin", "time_start", "time_end")

class SpecialPollVotersAdmin(admin.ModelAdmin):
    list_display = ("special_poll", "name", "time_requested", "allowed", "voted")

class SpecialPollContestantsAdmin(admin.ModelAdmin):
    list_display = ("poll", "name", "votes")

admin.site.register(Poll, PollAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(SpecialPoll, SpecialPollAdmin)
admin.site.register(SpecialPollVoters, SpecialPollVotersAdmin)
admin.site.register(SpecialPollContestants, SpecialPollContestantsAdmin)