from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.utils import timezone
from .models import *
from django.urls import reverse_lazy
from django.views import generic
from .forms import *
from django.contrib.auth.views import PasswordResetView
# start for email setting _signup
from django.template.loader import get_template
from django.core.mail import  EmailMultiAlternatives
from django.conf import settings
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
#end of email setting_sign up
from hashlib import sha1
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

now = timezone.now()
def home(request):
   return render(request, 'shop/home.html',
                 {'shope': home})



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
    user = ''
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
                if  User.objects.filter(username=username).exists():
                    # user exists
                    user = User.objects.filter(username=username).first()
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.last_login is not None:
                            return redirect('nca:home')
                        else:
                            password_change_form = PasswordChangeForm(user=user)
                            return render(request,'registration/password_change_form.html',{"username":username,"form":password_change_form})
                    else:
                        error = "please enter your username and password"
                        return render(request, 'registration/login.html', {"username": username, "password": password, "error": error})

                else:
                    #show signup form
                    error = "username not exists please create a new account"
                    return render(request, 'registration/login.html', {"username": username, "password": password, "error": error})
        else:
                error="please enter your username and password"
                return render(request,'registration/login.html',{"username":username,"password": password,"error":error})

    return render(request,'registration/login.html')


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

def sendEmail_signup(email, pwd, username):
    img_data = open(settings.STATIC_ROOT + "/img/NCA_Logo.png", 'rb').read()
    html_part = MIMEMultipart(_subtype='related')
    # Now create the MIME container for the image
    img = MIMEImage(img_data, 'jpeg')
    img.add_header('Content-Id', '<myimage>')  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="myimage")  # David Hess recommended this edit
    html_part.attach(img)

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
    message.attach(html_part)
    message.send()

class PasswordResetNCAEmailView(PasswordResetView):
    PasswordResetView.extra_email_context = {'nca_site_name': 'Nebraska Cancer Association'}
