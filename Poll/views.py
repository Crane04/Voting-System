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
    present_poll = Poll.objects.get(unique_id = pk)
    contestants = Option.objects.filter(poll = present_poll)

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
            if request.FILES:
                contestant = request.POST["contestant"]
                image =  request.FILES["image"]
                add_option = Option.objects.create(
                    poll = present_poll,
                    name = contestant,
                    option_image = image
                )
                add_option.save()
                return redirect("/poll/"+pk)
            else:
                messages.info(request, "You must insert an Image.")
                return redirect("/poll/" + pk)

        else:

            # Voting Process
            if Voter.objects.filter(poll = present_poll, user = user).exists():
                messages.info(request, "Sorry, you've voted before!")
            else:
                contestant_id = request.POST.get('vote')
                
                if contestant_id:
                    contestant = Option.objects.get(id = contestant_id)
                    voter = Voter.objects.create(poll = present_poll, user = user)
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