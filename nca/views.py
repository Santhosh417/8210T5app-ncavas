from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils import timezone
from events.models import Event, Enrollment, Location
from users.models import User


def home(request):
    upcoming_events = Event.objects.filter(volunteer_id=request.user.id, start_date_time__gte=timezone.now())
    now = datetime.today()
    now = now.replace(second=0, microsecond=0)
    current_event_ids = []

 # set end of the day based on end date time for events
    for event in Event.objects.all():
        eod = datetime(
            year=event.end_date_time.year,
            month=event.end_date_time.month,
            day=event.end_date_time.day) + timedelta(days=1, microseconds=-1)
        if eod > now:
            current_event_ids.append(event.event_id)

        # getting the current happening events and merging to events
    current_events = Event.objects.filter(event_id__in=current_event_ids)
    events = upcoming_events | current_events
    events = events.order_by("end_date_time")


    for x in events:
        print(x.event_id)
        enrollments = Enrollment.objects.filter(event_id=x.event_id)
        location = Location.objects.filter(location_id=x.location_id)
        victims = []
        for y in enrollments:
            victims += list(User.objects.filter(id=y.victim_id))
        x.victims = victims
        print(x.victims)
    return render(request, 'home.html', {'events': events})


def workinprogress(request):
        return render(request, 'workInProgress.html')

def contactus(request):
        return render(request, 'ContactUs.html')