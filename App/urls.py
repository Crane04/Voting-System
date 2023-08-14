from .views import *
from django.urls import path

urlpatterns = [
    path("", index, name = "index"),   
    path("new", new, name = "new"),
    path("mypolls", mypolls, name = "mypolls"),
    path("followpolls", followpolls, name = "followpolls"),
]