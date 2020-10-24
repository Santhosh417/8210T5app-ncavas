from . import views
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import signup_volunteer



app_name = 'users'

urlpatterns = [
    path('signup/', signup_volunteer, name='signup'),
    path('edit/<int:pk>', views.edit_volunteer, name='edit_volunteer'),
    path('volunteer_list/', views.volunteer_list, name='volunteer_list'),
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('about_page/', views.about, name='about'),
    path('accounts/login/', views.login, name='login'),
    path('faq_page/', views.faq, name='faq'),
    #path('', include('django.contrib.auth.urls')),
    path('password_reset_form/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset_form'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('users/password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

]
