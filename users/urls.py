from . import views
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import signup_volunteer, PasswordResetNCAEmailView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView,\
    PasswordResetDoneView, PasswordResetConfirmView


app_name = 'users'

urlpatterns = [
    path('signup/', signup_volunteer, name='signup'),
    path('edit/<int:pk>', views.edit_volunteer, name='edit_volunteer'),
    path('volunteer_list/', views.volunteer_list, name='volunteer_list'),
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    # path('about_page/', views.about, name='about'),
    path('accounts/login/', views.loginView, name='login'),
    # path('faq_page/', views.faq, name='faq'),
    # path('faq_page/', views.faq, name='faq'),
    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('change-password-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset-form/', PasswordResetNCAEmailView.as_view(), name='password_reset_form'),
    path('password-reset-done-form/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
