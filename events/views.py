from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.utils import timezone
from django.db.models import Q

from users.forms import VolunteerSignUpForm, VolunteerForm
from .forms import *

now = timezone.now()
def home(request):
   return render(request, 'shop/home.html',
                 {'shope': home})

def register_volunteer(request):
    if request.method == 'POST':
        form = VolunteerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('users:volunteer_list')
            else:
                return render(request, 'registration/registration_done.html')
    args = {}
    args.update(csrf(request))
    args['form'] = VolunteerSignUpForm()
    return render(request, 'registration/volunteer_registration_form.html', args)


# @login_required
# def edit_volunteer(request, pk):
#     volunteer = get_object_or_404(User, pk=pk)
#     if request.method == "POST":
#         # update
#         form = VolunteerForm(request.POST, instance=volunteer)
#         if form.is_valid():
#             volunteer = form.save(commit=False)
#             volunteer.save()
#             return redirect('users:volunteer_list')
#     else:
#         # edit
#         form = VolunteerForm(instance=volunteer)
#     return render(request, 'users/volunteer_edit.html', {'form': form})



def volunteer_list(request):
    volunteers = User.objects.filter(is_customer=True)
    return render(request, 'volunteer_list.html',
                  {'volunteers': volunteers})


def home(request):
    return render(request, 'stitchmaster/stitchmaster_homepage.html',
                  {'home': home})


def about(request):
    return render(request, 'stitchmaster/about_page.html',
                  {'about': about})


def faq(request):
    return render(request, 'stitchmaster/faq_page.html',
                  {'faq': faq})


def login(request):
    return render(request, 'registration/login.html',
                  {'login': login})


# produces public events page
def events_details(request, **kwargs):
    now= datetime.today()
    ongoing_events_date = Event.objects.filter(start_date_time__date=now,event_type ='Public')
    upcoming_events_date = Event.objects.filter(start_date_time__date__gt=now, event_type ='Public')

    return render(request, 'eventsPage.html', {'now': now,'ongoing_events':ongoing_events_date,'upcoming_events': upcoming_events_date})

# To view event notes for admins
def events_notes(request, **kwargs):
    now= datetime.today()
    old_events = Event.objects.filter(end_date_time__date__lt=now)
    enrollments = Enrollment.objects.filter(Q(event__in=old_events))
    return render(request, 'event_notes.html', {'now': now,'enrollments':enrollments})



# method for volunteer to take event notes Nov 6

# show the event notes by volunteer
def showevent_meetingnotes(request,pk):
    event = Event.objects.filter(event_id=pk).first()
    enrollments = Enrollment.objects.filter(event_id=pk)
    form = VolunteerMeetingNotesForm(initial=event)
    # setting the time to show the events to be able to add/edit until end of the day
    now = datetime.today()
    now = now.replace(second=0, microsecond=0)
    eod = datetime(
        year=event.end_date_time.year,
        month=event.end_date_time.month,
        day=event.end_date_time.day
    ) + timedelta(days=1, microseconds=-1)

    return render(request, 'MakeMeetingnotes.html', {'form': form,'enrollments':enrollments,'eod':eod,'now':now})

## add/edit victims meeting notes for the event by volunteer
def add_meetingnotes(request, pk):
    enrollment = Enrollment.objects.filter(enrollment_id=pk).first()

    if request.method == 'POST':
        form = AddMeetingNotesForm(request.POST, instance=enrollment)
        if form.is_valid():
            add_enrollment=form.save(commit=False)
            add_enrollment.event= enrollment.event
            add_enrollment.victim= enrollment.victim
            add_enrollment.save()

            return render(request, 'AddMeetingnotes_successful.html', {'enrollment': enrollment})
        else:
            return render(request, 'AddMeetingnotes.html', {'form': form,'victim':enrollment.victim,'event':enrollment.event })

    else:
        form = AddMeetingNotesForm(instance=enrollment)
        return render(request, 'AddMeetingnotes.html', {'form': form,'victim':enrollment.victim,'event':enrollment.event})

@login_required
def add_meeting(request):
    victims = Victim.objects.all()
    if request.method == "POST":
        volunteer = get_object_or_404(Volunteer, pk=request.user.id)
        updated_data = request.POST.copy()
        updated_data.update({'start_date_time': datetime.strptime(request.POST.get("start_date_time"), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')})
        updated_data.update({'end_date_time': datetime.strptime(request.POST.get("end_date_time"), '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')})
        form = VolunteerScheduleMeeting(data=updated_data)
        if form.is_valid():
            event = form.save(volunteer, request.POST.getlist("victims"),request.POST.get("event_type"))
            return render(request, 'meetingCreated_successful.html', {'event': event})
    else:
        form = VolunteerScheduleMeeting()
    return render(request, 'createMeeting.html', {'form': form, 'victims': victims})


