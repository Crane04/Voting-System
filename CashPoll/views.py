from django.shortcuts import render, redirect
from .models import *
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Count
from App.views import datetime_to_seconds
import time

def poll(request, pk):
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
            return redirect("/poll/"+pk)


        else:

            # Voting Process
            if CashPollVoter.objects.filter(poll = present_poll, user = user).exists():
                messages.info(request, "Sorry, you've voted before!")
            else:
                contestant_id = request.POST.get('vote')
                
                if contestant_id:
                    contestant = CashPollOption.objects.get(id = contestant_id)
                    voter = CashPollVoter.objects.create(poll = present_poll, user = user)
                    contestant.votes += 1
                    contestant.save()
                    voter.save()
            return redirect("/poll/"+pk)
    context = {
            "poll": present_poll,
            "contestants":contestants,
            "start_voting_process": start_voting_process,
            # "messages": messages
        }
        
    return render(request, "normal poll/present-poll.html", context)