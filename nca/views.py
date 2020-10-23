from django.shortcuts import render
from django.utils import timezone
from events.models import Event, Enrollment, Location
from users.models import User


def home(request):
        events = Event.objects.filter(volunteer_id=request.user.id, start_date_time__gte= timezone.now())
        for x in events:
                print(x.event_id)
                enrollments = Enrollment.objects.filter(event_id = x.event_id)
                location = Location.objects.filter(location_id=x.location_id)
                victims = []
                for y in enrollments:
                        victims += list(User.objects.filter(id = y.victim_id))
                x.victims = victims
                print(x.victims)
        return render(request, 'home.html', {'events': events})


def workinprogress(request):
        return render(request, 'workInProgress.html')

