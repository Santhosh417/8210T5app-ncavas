from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Volunteer, User


class VolunteerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile_num', 'username', 'password1', 'password2')

    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        Volunteer.objects.create(user=user)
        return user


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile_num')


