from django.shortcuts import render, redirect
from Poll.models import *
from SpecialPoll.models import *
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Count
from datetime import datetime, timezone
from django.core.mail import send_mail
from django.conf import Settings
import pytz

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




def datetime_to_seconds(date_time):
    if date_time is not None:
        # Calculate seconds since the Unix epoch (January 1, 1970)
        epoch = datetime(1970, 1, 1, tzinfo=date_time.tzinfo)
        timedelta = date_time - epoch
        timestamp_seconds = int(timedelta.total_seconds()) - 3600
        return timestamp_seconds
    else:
        return None  # Handle case where datetime is None


def sendmail(receiver, poll, link):
    subject = f" Poll Approval"
    message = ''
    from_email = 'encrane04@gmail.com'  # Sender's email
    recipient_list = [receiver]  # List of recipient emails
    html_message = f"""<div style="text-align:center; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">
    <h1 style="color:blue;"> You've been allowed to view and vote on this Poll {poll}</h1>
    <h3>Click <a href="http://127.0.0.1:8000/special-poll/{link}"> here </a> to continue</h1>
    <br><br><br><br>
    
    <p>&copy; Vote It!, 2023 </h1>
    </div>
    """
    fail_silently = False
    send_mail(subject, message, from_email, recipient_list, fail_silently, html_message=html_message)