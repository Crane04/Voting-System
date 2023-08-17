from .views import *
from django.urls import path

urlpatterns = [
    path("cashpoll/<str:pk>", cashpoll, name = "cashpoll"),
    path("pay", pay, name = "pay"),
]