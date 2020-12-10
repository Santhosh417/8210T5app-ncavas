from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Volunteer, User, SpecializedInChoices


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
    specialized_in = forms.ModelMultipleChoiceField(label='Specialized in?', queryset=SpecializedInChoices.objects.all(), required=False,
                                                    widget=forms.CheckboxSelectMultiple,)
    class Meta:
        model = Volunteer
        fields = ('first_name', 'last_name', 'email', 'mobile_num',
                  'work_phone', 'street_address', 'city', 'state', 'zip',
                  'time_spent', 'specialized_in')

    def __init__(self, *args, **kwargs):
        super(VolunteerForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True

class VolunteerCreationForm(UserCreationForm):
    TIME_SPENT_CHOICE = [
        ('> 5 hours (~ 7 hours)', '> 5 hours (~ 7 hours)'),
        ('< 5 hours (~ 2 hours)', '< 5 hours (~ 2 hours)'),
        ( "Don't mind", "Don't mind"),
    ]

    time_spent = forms.ChoiceField(required= False, label='How much time can you get involved per week?', choices=TIME_SPENT_CHOICE, widget=forms.RadioSelect())
    specialized_in = forms.ModelMultipleChoiceField(label='Specialized in?', queryset=SpecializedInChoices.objects.all(), required=False,
                                                    widget=forms.CheckboxSelectMultiple,)
    comments = forms.CharField(required= False,label='',
                    widget=forms.Textarea(attrs={'placeholder': 'Additional Information'}))
    class Meta(UserCreationForm):
        model = Volunteer
        fields = ('first_name', 'last_name', 'email','mobile_num', 'work_phone', 'street_address', 'city', 'state',
                  'zip', 'time_spent', 'specialized_in', 'comments',)

    def __init__(self, *args, **kwargs):
        super(VolunteerCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password1')
        self.fields.pop('password2')

    def save(self, commit=True, uname="unknown", pword="unknown"):
        self.cleaned_data['password1'] = pword
        volunteer = super(VolunteerCreationForm, self).save(commit=False)
        volunteer.username = uname
        volunteer.first_name = self.cleaned_data['first_name']
        volunteer.last_name = self.cleaned_data['last_name']

        if commit:
            volunteer.save()
        return volunteer

