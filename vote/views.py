from django.shortcuts import render, redirect
from .models import *
import uuid
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        title =  request.POST["poll_name"]
        time_start = request.POST["poll_st"]
        time_end = request.POST["poll_end"]
        unique_id = uuid.uuid4()

        create_poll = Poll.objects.create(unique_id = unique_id,
        title = title, 
        time_start = time_start,
        time_end = time_end,
        admin = user)
        create_poll.save()

        return redirect("/poll/" + str(unique_id))

    return render(request,"index.html")
    
def poll(request, pk):
    present_poll = Poll.objects.get(unique_id = pk)
    contestants = Option.objects.filter(poll = present_poll)

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
            contestant_id = request.POST.get('contestant_id')
            if contestant_id:
                contestant = Option.objects.get(id = contestant_id)
                contestant.votes += 1
                contestant.save()
                return redirect("/poll/"+pk)
    context = {
            "poll": present_poll,
            "contestants":contestants
        }
        


        
    return render(request, "poll.html", context)