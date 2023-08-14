from .views import *
from django.urls import path

urlpatterns = [
    path("special-poll/<str:pk>", specialpoll)
]