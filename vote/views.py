from django.shortcuts import render, redirect
from .models import *
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Count
# Create your views here.

def index(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        title =  request.POST["poll_name"]
        time_start = request.POST["poll_st"]
        time_end = request.POST["poll_end"]
        unique_id = uuid.uuid4()
        description  = request.POST["description"]
        who_can_vote = request.POST["who_can_vote"]

        if who_can_vote == "anyone":

            create_poll = Poll.objects.create(unique_id = unique_id,
            title = title, 
            time_start = time_start,
            time_end = time_end,
            admin = user,
            description = description
            )
            create_poll.save()
            return redirect("/poll/" + str(unique_id))
        
        elif who_can_vote == "registered":

            create_special_poll = SpecialPoll.objects.create(unique_id = unique_id,
            title = title, 
            time_start = time_start,
            time_end = time_end,
            admin = user,
            description = description
            )
            create_special_poll.save()
            return redirect("/special-poll/" + str(unique_id))


    return render(request,"index.html")

def new(request):
    return index(request)


def poll(request, pk):
    present_poll = Poll.objects.get(unique_id = pk)
    contestants = Option.objects.filter(poll = present_poll)
    current_datetime = timezone.now()
    start_poll = present_poll.time_start
    end_poll = present_poll.time_end
    user = User.objects.get(username=request.user.username)

    start_voting_process = None
    if current_datetime >= start_poll and current_datetime <= end_poll:
        start_voting_process = True
    elif current_datetime < start_poll and current_datetime > end_poll:
        start_voting_process = False

    if request.method == "POST":
        # Add Contestant Request
        if "add_contestant" in request.POST:
            contestant = request.POST["contestant"]
            add_option = Option.objects.create(
                poll = present_poll,
                name = contestant
            )
            add_option.save()
            return redirect("/special-poll/"+pk)


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


def mypolls(request):

    user = User.objects.get(username=request.user.username)

    polls_by_user = Poll.objects.filter(admin=user).order_by("title")
    polls_with_voter_counts = polls_by_user.annotate(num_voters=Count('voter'))

    special_polls_by_user = SpecialPoll.objects.filter(admin=user).order_by("title")
    special_polls_with_voter_counts = special_polls_by_user.annotate(num_voters=Count('specialpollvoters'))

    context = {
        'user': user,
        'polls_with_voter_counts': polls_with_voter_counts,
        'special_polls_with_voter_counts': special_polls_with_voter_counts
    }

    return render(request, "mypolls.html", context)


def followpolls(request):
    user = User.objects.get(username=request.user.username)
    follow_polls = Voter.objects.filter(user = user).order_by("poll")

    context = {
        "followpolls": follow_polls
    }

    return render(request, "followpolls.html", context)


def specialpoll(request, pk):
    user = User.objects.get(username=request.user.username)
    present_poll = SpecialPoll.objects.get(unique_id = pk)

    contestants = SpecialPollContestants.objects.filter(poll = present_poll)
    current_datetime = timezone.now()
    start_poll = present_poll.time_start
    end_poll = present_poll.time_end
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