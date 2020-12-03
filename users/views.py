from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import *

now = timezone.now()
def home(request):
   return render(request, 'shop/home.html',
                 {'shope': home})



@login_required
def edit_volunteer(request, pk):
    volunteer = get_object_or_404(Volunteer, pk=pk)
    if request.method == "POST":
        # update
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.save()
            form.save_m2m()
            specialized_choices = volunteer.specialized_in.all()
            specialized_choices_str = ''
            for choice in specialized_choices:
                    specialized_choices_str += str(choice)
                    specialized_choices_str += ','
            volunteer.specialized_choices =  specialized_choices_str[:-1]
            return render(request, 'volunteer_detail.html',
                  {'object': volunteer})
    else:
        # edit
        form = VolunteerForm(instance=volunteer)
    return render(request, 'volunteer_edit.html', {'form': form})

def volunteer_list(request):
    volunteers = User.objects.filter(is_customer=True)
    return render(request, 'volunteer_list.html',
                  {'volunteers': volunteers})

# method for volunteer log in using OTP sent in email
def loginView(request):
    user = ''
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.last_login:
                    login(request, user)
                    return redirect('nca:home')
                else:
                    login(request, user)
                    #user.last_login = timezone.now()
                    #password_change_form = PasswordChangeForm(user=user)
                    return redirect('users:password_change')
            else:
                #show signup form
                error = "username not exists please create a new account"
                return render(request, 'registration/login.html', {"username": username, "password": password, "error": error})
        else:
                error="please enter your username and password"
                return render(request,'registration/login.html',{"username":username,"password": password,"error":error})

    return render(request,'registration/login.html')

# method for volunteer sign up
def signup_volunteer(request):
    if request.method == 'POST':
        u = request.POST.get('first_name', '').lower() + "." + request.POST.get('last_name', '').lower();
        e = request.POST.get('email')
        p = User.objects.make_random_password(length=8)
        form = VolunteerCreationForm(request.POST)

        if form.is_valid():
            form.save(uname=u, pword=p)
            form.save_m2m()
            sendEmail_signup(e,p,u)
            return render(request, 'registration/signup_email.html')

        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = VolunteerCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# method for sending email after volunteer registration
def sendEmail_signup(email, pwd, username):
    # img_data = open(settings.STATIC_ROOT + "/img/NCA_Logo.PNG", 'rb').read()
    #  html_part = MIMEMultipart(_subtype='related')
    # Now create the MIME container for the image
    # img = MIMEImage(img_data, 'jpeg')
    # img.add_header('Content-Id', '<myimage>')  # angle brackets are important
    # img.add_header("Content-Disposition", "inline", filename="myimage")  # David Hess recommended this edit
    # html_part.attach(img)

    subject = "Welcome to Nebraska Cancer Association"
    content = {'pwd': pwd, 'uname': username, 'nca_site_name': 'Nebraska Cancer Association'}
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    with open("nca/templates/registration/email_review_signup.txt") as f:
        signup_message = f.read()
    message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email,
                                     to=[to_email], )
    html_template = get_template("registration/signup_email_body.html").render(context=content)
    message.attach_alternative(html_template, "text/html")
    # message.attach(html_part)
    message.send()

# updating the website name for password reset email
class PasswordResetNCAEmailView(PasswordResetView):
    PasswordResetView.extra_email_context = {'nca_site_name': 'Nebraska Cancer Association'}

# method to make volunteer subscribe to NCA Newsletter
@login_required()
def newsletter_subscribe(request):
    volunteer = Volunteer.objects.get(id=request.user.id)
    volunteer.is_subscribed=True
    volunteer.save()
    ############# mail for newsletter successful subscription
    name=volunteer.first_name
    subject = "Subscription to Nebraska Cancer Association"
    from_email = settings.EMAIL_HOST_USER
    to_email = request.user.email
    context={'vname': name, 'nca_site_name': 'Nebraska Cancer Association'}
    message = EmailMultiAlternatives(subject=subject, from_email=from_email,
                                     to=[to_email])
    html_template = get_template("subscription_mail.html").render(context=context)
    message.attach_alternative(html_template, "text/html")
    message.attach_file("nca/static/img/Newsletter.pdf", mimetype="application/pdf")
    message.send()
    return redirect(reverse_lazy('nca:contactus'))

# method to make volunteer unsubscribe to NCA Newsletter
@login_required()
def newsletter_unsubscribe(request):
    volunteer = Volunteer.objects.get(id=request.user.id)
    volunteer.is_subscribed = False
    volunteer.save()
    return redirect(reverse_lazy('nca:contactus'))
