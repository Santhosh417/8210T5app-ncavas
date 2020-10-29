import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.utils import timezone

from users.forms import VolunteerSignUpForm, VolunteerForm
from .models import *
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


@login_required
def edit_volunteer(request, pk):
    volunteer = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        # update
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.save()
            return redirect('shop:product_list')
    else:
        # edit
        form = VolunteerForm(instance=volunteer)
    return render(request, 'registration/volunteer_edit.html', {'form': form})



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
    now= datetime.datetime.today()
    ongoing_events_date = Event.objects.filter(start_date_time__date=now,event_type ='Public')
    upcoming_events_date = Event.objects.filter(start_date_time__date__gt=now, event_type ='Public')

    return render(request, 'eventsPage.html', {'now': now,'ongoing_events':ongoing_events_date,'upcoming_events': upcoming_events_date})