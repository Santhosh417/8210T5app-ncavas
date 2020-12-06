from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from nca import views


app_name = 'nca'
urlpatterns = [
    path('', views.home, name="home"),
    path('workinprogress/', views.workinprogress, name="workinprogress"),
    path('contactus/', views.contactus, name="contactus"),
    path('faq/', views.faq, name="faq"),
    path('victim-stories/', views.victimStories, name="victim-stories"),
    path('volunteer-stories/', views.volunteerStories, name="volunteer-stories")
]
