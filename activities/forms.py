from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Location


# class LocationSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model = Location
#         fields = ('name', 'address', 'city', 'state', 'zip')
#
#     def save(self):
#         Location.objects.create(user=user)
#         return
#
#
# class LocationForm(forms.ModelForm):
#     class Meta:
#         model = Location
#         fields = ('name', 'address', 'city', 'state', 'zip')
