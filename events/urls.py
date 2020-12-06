from . import views
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views



app_name = 'events'

urlpatterns = [
    re_path(r'register_event/', views.register_volunteer, name='register_event'),
    # path('edit/<int:pk>', views.edit_event, name='edit_event'),
    # path('event_list/', views.event_list, name='event_list'),
    path('events_details/', views.events_details, name='events_details'),
    path('events_notes/', views.events_notes, name='events_notes'),
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('about_page/', views.about, name='about'),
    path('showevent_meetingnotes/<int:pk>/',views.showevent_meetingnotes, name='showevent_meetingnotes'),
    path('add_meetingnotes/<int:pk>/',views.add_meetingnotes, name='add_meetingnotes'),
    path('add_meetingnotes_success/<int:pk>/',views.add_meetingnotes, name='add_meetingnotes_success'),
    path('meeting_create/', views.add_meeting, name='add_meeting'),

]
