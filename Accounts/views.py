from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == "POST":
        username =  (request.POST["username"]).lower()
        email =  (request.POST["email"]).lower()
        password1 =  request.POST["password_signin1"]
        password2=  request.POST["password_signin2"]

        if password1 != password2:
            messages.info(request, "Passwords don't match!")
            return redirect("/")

        else:
            if User.objects.filter(username = username).exists():
                messages.info(request, "Username already exists")
                return redirect("/register")

            elif User.objects.filter(email = email).exists():
                messages.info(request, "Email Already Exists!")
                return redirect("/register")

            else:
                user = User.objects.create(username = username, email = email, password = password1)
                user.save()
    
            return redirect("/")

    return render(request, "Accounts/register.html")

def login_(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password_signin"]

        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Incorrect Credentials!")
            return redirect("/login")

    return render(request,"Accounts/login.html")

def logout_(request):
    logout(request)
    return redirect("/login")
    

