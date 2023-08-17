from django.shortcuts import render, redirect
from .models import *
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Count
from App.views import datetime_to_seconds
import time
from django.conf import settings

def cashpoll(request, pk):
    present_poll = CashPoll.objects.get(unique_id = pk)
    contestants = CashPollOption.objects.filter(poll = present_poll)

    current_datetime = time.time()
    poll_starts = datetime_to_seconds(present_poll.time_start)
    poll_ends = datetime_to_seconds(present_poll.time_end)

    user = User.objects.get(username=request.user.username)


    
    start_voting_process = None
    if current_datetime >= poll_starts and current_datetime <= poll_ends:
        start_voting_process = True
    elif current_datetime < poll_starts and current_datetime > poll_ends:
        start_voting_process = False

    if request.method == "POST":
        # Add Contestant Request
        if "add_contestant" in request.POST:
            contestant = request.POST["contestant"]
            add_option = CashPollOption.objects.create(
                poll = present_poll,
                name = contestant
            )
            add_option.save()
            return redirect("/cashpoll/"+pk)


        else:

            contestant_id = request.POST.get('vote')
            
            if contestant_id:
                contestant = CashPollOption.objects.get(id = contestant_id)
                contestant.votes += 1
                contestant.save()
        return redirect("/cashpoll/"+pk)
    context = {
            "poll": present_poll,
            "contestants":contestants,
            "start_voting_process": start_voting_process,
            # "messages": messages
        }
        
    return render(request, "cash poll/present-poll.html", context)

def pay(request):
    if request.method == "POST":


        pk = settings.PAYSTACK_PUBLIC_KEY


        context = {
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': 100000,
        }

    return render("paystack.html")

def verify_payment(request):

    if True:
        print("okay")
        return redirect("/")

    else:
        print("bad")