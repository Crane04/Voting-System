from django.contrib import admin
from .models import *
# Register your models here.

class PollAdmin(admin.ModelAdmin):
    list_display = ("admin","title", "time_start", "time_end")

class OptionAdmin(admin.ModelAdmin):
    list_display = ("poll", "name", "votes")

admin.site.register(Poll, PollAdmin)
admin.site.register(Option, OptionAdmin)