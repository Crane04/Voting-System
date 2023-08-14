from django.shortcuts import render, redirect
from Poll.models import *
from SpecialPoll.models import *
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Count

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