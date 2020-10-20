from . import views
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views



app_name = 'users'

urlpatterns = [
    re_path(r'register_event/', views.register_volunteer, name='register_event'),
    path('edit/<int:pk>', views.edit_event, name='edit_event'),
    path('event_list/', views.event_list, name='event_list'),
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('about_page/', views.about, name='about'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

]