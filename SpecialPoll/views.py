from django.shortcuts import render, redirect
from .models import *
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Count
from App.views import datetime_to_seconds
import time

# Create your views here.
def specialpoll(request, pk):
    user = User.objects.get(username=request.user.username)
    present_poll = SpecialPoll.objects.get(unique_id = pk)

    contestants = SpecialPollContestants.objects.filter(poll = present_poll)
    current_datetime = time.time()
    start_poll = datetime_to_seconds(present_poll.time_start)
    end_poll = datetime_to_seconds(present_poll.time_end)
    unauthorized = None
    unapproved_voters = SpecialPollVoters.objects.filter(allowed = False, special_poll = present_poll)

    start_voting_process = None
    if current_datetime >= start_poll and current_datetime <= end_poll:
        start_voting_process = True
    elif current_datetime < start_poll and current_datetime > end_poll:
        start_voting_process = False

    if SpecialPollVoters.objects.filter(name = user, allowed=True).exists():
        unauthorized = False
    else:
        unauthorized = True

    if request.method == "POST":
        if "request" in request.POST:
            request_vote = SpecialPollVoters.objects.create(name = user,
            special_poll = present_poll)
            request_vote.save()
            return redirect("/special-poll/" +  pk)

        # Add Contestant Request
        elif "add_contestant" in request.POST:
            print(8)
            contestant = request.POST["contestant"]
            add_option = SpecialPollContestants.objects.create(
                poll = present_poll,
                name = contestant
            )
            add_option.save()
            return redirect("/special-poll/"+pk)

        elif "confirm" in request.POST:

            unapproved = request.POST.get("approve")
            approve = SpecialPollVoters.objects.get(special_poll = present_poll, id = unapproved)
            approve.allowed = True
            approve.save()
            return redirect("/special-poll/" + pk)

        elif "requestvote" in request.POST:
            if SpecialPollVoters.objects.filter(name = user, special_poll  = present_poll, allowed = False).exists():
                messages.info(request, "You've applied already, you'll be notified once the Admin approves you.")

            elif SpecialPollVoters.objects.filter(name = user, special_poll  = present_poll, allowed = True).exists():
                messages.info(request, "You've been approved already.")
            else:
                special_poll_voter = SpecialPollVoters.objects.create(name = user, special_poll = present_poll)
                special_poll_voter.save()

            return redirect("/special-poll/" + pk)
            

        elif "vote" in request.POST:

            # Voting Process

            if SpecialPollVoters.objects.filter(special_poll = present_poll, name = user, voted = True).exists():
                messages.info(request, "Sorry, you've voted before!")
            else:
                contestant_id = request.POST.get('voting')
                print(contestant_id)
                if contestant_id:
                    contestant = SpecialPollContestants.objects.get(id = contestant_id)
                    voter = SpecialPollVoters.objects.get(special_poll = present_poll, name = user, voted = False)
                    contestant.votes += 1
                    voter.voted = True
                    contestant.save()
                    voter.save()
            return redirect("/special-poll/"+pk)
    context = {
            "poll": present_poll,
            "contestants":contestants,
            "start_voting_process": start_voting_process,
            "unapproved_voters": unapproved_voters,
            "unauthorized": unauthorized
        }
        
    return render(request, "special poll/present-poll.html", context)