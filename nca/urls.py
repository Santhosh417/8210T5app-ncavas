from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from nca import views

urlpatterns = [
    path('', views.home, name="home")
]
