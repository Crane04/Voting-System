from django.contrib import admin
from .models import *
# Register your models here.

class PollAdmin(admin.ModelAdmin):
    list_display = ("title","admin", "time_start", "time_end")

class OptionAdmin(admin.ModelAdmin):
    list_display = ("poll", "name", "votes")

class VoterAdmin(admin.ModelAdmin):
    list_display = ("poll", "user")

    
admin.site.register(Poll, PollAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Voter, VoterAdmin)