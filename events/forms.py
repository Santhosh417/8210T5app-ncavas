from datetime import timedelta

from django import forms
from django.forms import HiddenInput
from django.shortcuts import get_object_or_404
from .models import *

## form to display volunteer meeting notes Nov 10
class VolunteerMeetingNotesForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields=('victim','notes')
        widgets ={
            'notes': forms.Textarea(attrs={'placeholder': 'Add notes..',})
        }


    meeting_name = forms.CharField(max_length=100, label="Meeting_Name")
    meeting_time = forms.DateTimeField(label="Meeting_Time")
    location = forms.CharField(max_length=100, label="Meeting_Location")
    address = forms.CharField(max_length=100, label="Meeting_address")
    city = forms.CharField(max_length=100, label="Meeting_city")
    state = forms.CharField(max_length=100, label="Meeting_state")
    zip = forms.CharField(max_length=100, label="Meeting_ zip code")

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('initial', None)
        super(VolunteerMeetingNotesForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['meeting_name'].widget.attrs['readonly'] = True
            self.fields['meeting_time'].widget.attrs['readonly'] = True
            self.fields['location'].widget.attrs['readonly'] = True
            self.fields['address'].widget.attrs['readonly'] = True
            self.fields['state'].widget.attrs['readonly'] = True
            self.fields['city'].widget.attrs['readonly'] = True
            self.fields['zip'].widget.attrs['readonly'] = True
            self.fields['notes'].widget = HiddenInput()
            self.fields['victim'].widget = HiddenInput()

            self.fields['meeting_time'].initial = str(instance.start_date_time.replace(tzinfo=None) - timedelta(hours=18))+ "-" + str(instance.end_date_time.replace(tzinfo=None) - timedelta(hours=18))
            self.fields['meeting_name'].initial = instance.event_name
            self.fields['location'].initial = instance.location
            self.fields['address'].initial = instance.location.address
            self.fields['state'].initial = instance.location.state
            self.fields['city'].initial = instance.location.city
            self.fields['zip'].initial = instance.location.zip
            self.fields['notes'].initial = None


# form for adding/editing victims meeting notes by volunteer Nov 10
class AddMeetingNotesForm(forms.ModelForm):

    class Meta:
        model = Enrollment
        fields=('notes','is_important')
        widgets ={
            'notes': forms.Textarea(attrs={'placeholder': 'Add notes..',}),
            # 'is_important':forms.BooleanField(required=False),
        }

    def __init__(self, *args, **kwargs):
        super(AddMeetingNotesForm, self).__init__(*args, **kwargs)
        self.fields['notes'].label = ''

class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)

class VolunteerScheduleMeeting(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_name', 'start_date_time','end_date_time', 'description', 'staff', 'location')
        widgets = {
            'start_date_time': DateTimeInput(),
            'end_date_time': DateTimeInput(),
            'description': forms.Textarea(attrs={'placeholder': 'Add description..', })
        }

    def save(self, volunteer, victims, event_type):
        event = super().save(commit=False)
        event.volunteer = volunteer
        event.event_type = event_type
        event.save()
        for x in victims:
            v = get_object_or_404(Victim, pk=x)
            Enrollment.objects.create(event = event,victim=v)
        return event
