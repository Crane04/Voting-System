from django.contrib import admin
from .models import *
# Register your models here.

class CashPollAdmin(admin.ModelAdmin):
    list_display = ("title","admin", "time_start", "time_end", "fee")

class CashPollOptionAdmin(admin.ModelAdmin):
    list_display = ("poll", "name", "votes")
    
admin.site.register(CashPoll, CashPollAdmin)
admin.site.register(CashPollOption, CashPollOptionAdmin)