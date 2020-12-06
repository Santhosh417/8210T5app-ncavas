from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils import timezone
from events.models import Event, Enrollment, Location
from users.models import User, Volunteer
import pytz
from django.conf import settings

def home(request):
    upcoming_events = Event.objects.filter(volunteer_id=request.user.id, start_date_time__gte=timezone.now())
    now = datetime.today()
    now = now.replace(second=0, microsecond=0)
    current_event_ids = []

 # set end of the day based on end date time for events
    for event in Event.objects.all():
        end_date_time = event.end_date_time.astimezone(pytz.timezone(settings.TIME_ZONE))
        eod = datetime(
            year=end_date_time.year,
            month=end_date_time.month,
            day=end_date_time.day) + timedelta(days=1, microseconds=-1)
        if eod > now:
            current_event_ids.append(event.event_id)

    # getting the current happening events and merging to events
    current_events = Event.objects.filter(volunteer_id=request.user.id, event_id__in=current_event_ids)
    events = upcoming_events | current_events
    events = events.order_by("end_date_time")


    for x in events:
        enrollments = Enrollment.objects.filter(event_id=x.event_id)
        location = Location.objects.filter(location_id=x.location_id)
        victims = []
        for y in enrollments:
            victims += list(User.objects.filter(id=y.victim_id))
        x.victims = victims
    return render(request, 'home.html', {'events': events})


def workinprogress(request):
        return render(request, 'workInProgress.html')

# method for contact us page and volunteer subscription for newsletter
def contactus(request):
        template="ContactUs.html"
        volunteer = Volunteer.objects.filter(id=request.user.id).first()
        context = {'volunteer':volunteer}
        return render(request, template, context)

def faq(request):
        return render(request, 'faq.html')

def victimStories(request):
        return render(request, 'victim_story.html')

def volunteerStories(request):
        return render(request, 'volunteer_story.html')
