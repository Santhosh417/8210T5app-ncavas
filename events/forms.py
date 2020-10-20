from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Location, Enrollment
#
#
# class LocationSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model = Location
#         fields = ('name', 'address', 'city', 'state', 'zip')
#
# class LocationForm(forms.ModelForm):
#     class Meta:
#         model = Location
#         fields = ('name', 'address', 'city', 'state', 'zip')

# class EnrollmentCreateForm(forms.ModelForm):
#     class Meta:
#         model = Enrollment
#         fields = ['activity', 'victim', 'notes', 'is_important']
