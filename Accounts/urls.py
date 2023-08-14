from .views import *
from django.urls import path

urlpatterns = [
    path("register", register, name = "register"),
    path("login", login_, name = "login"),
]