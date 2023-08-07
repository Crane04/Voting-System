from django.shortcuts import render, redirect
from .models import *
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
# Create your views here.

def index(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        title =  request.POST["poll_name"]
        time_start = request.POST["poll_st"]
        time_end = request.POST["poll_end"]
        unique_id = uuid.uuid4()
        description  = request.POST["description"]

        create_poll = Poll.objects.create(unique_id = unique_id,
        title = title, 
        time_start = time_start,
        time_end = time_end,
        admin = user,
        description = description
        )
        create_poll.save()

        return redirect("/poll/" + str(unique_id))

    return render(request,"index.html")
    
def poll(request, pk):
    present_poll = Poll.objects.get(unique_id = pk)
    contestants = Option.objects.filter(poll = present_poll)
    current_datetime = timezone.now()
    start_poll = present_poll.time_start
    end_poll = present_poll.time_end
    print(current_datetime)
    start_voting_process = None
    if current_datetime >= start_poll and current_datetime <= end_poll:
        start_voting_process = True
    else:
        start_voting_process = False

    if request.method == "POST":
        if "add_contestant" in request.POST:
            contestant = request.POST["contestant"]
            add_option = Option.objects.create(
                poll = present_poll,
                name = contestant
            )
            add_option.save()
            return redirect("/poll/"+pk)
        else:
            contestant_id = request.POST.get('vote')
            if contestant_id:
                contestant = Option.objects.get(id = contestant_id)
                contestant.votes += 1
                contestant.save()
                return redirect("/poll/"+pk)
    context = {
            "poll": present_poll,
            "contestants":contestants,
            "start_voting_process": start_voting_process
        }
        


        
    return render(request, "present-poll.html", context)


def mypolls(request):

    user = User.objects.get(username=request.user.username)

    my_polls = Poll.objects.filter(admin = user)
    return render(request, "mypolls.html")