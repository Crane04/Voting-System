from .views import *
from django.urls import path

urlpatterns = [
    path("", index, name = "index"),
    path("poll/<str:pk>", poll, name = "poll")
]