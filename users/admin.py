from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ObjectDoesNotExist

from .models import Volunteer, Staff, Victim


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'work_phone')

    def username(self, instance):  # name of the method should be same as the field given in `list_display`
        try:
            return instance.user.username
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def first_name(self, instance):
        try:
            return instance.user.first_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def last_name(self, instance):
        try:
            return instance.user.last_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def email(self, instance):
        try:
            return instance.user.email
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def work_phone(self, instance):
        try:
            return instance.work_phone
        except ObjectDoesNotExist:
            return 'ERROR!!'


class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'work_phone')

    def username(self, instance):  # name of the method should be same as the field given in `list_display`
        try:
            return instance.user.username
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def first_name(self, instance):
        try:
            return instance.user.first_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def last_name(self, instance):
        try:
            return instance.user.last_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def email(self, instance):
        try:
            return instance.user.email
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def work_phone(self, instance):
        try:
            return instance.work_phone
        except ObjectDoesNotExist:
            return 'ERROR!!'

class VictimAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'disease_type')

    def username(self, instance):  # name of the method should be same as the field given in `list_display`
        try:
            return instance.user.username
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def first_name(self, instance):
        try:
            return instance.user.first_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def last_name(self, instance):
        try:
            return instance.user.last_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def email(self, instance):
        try:
            return instance.user.email
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def disease_type(self, instance):
        try:
            return instance.disease_type
        except ObjectDoesNotExist:
            return 'ERROR!!'

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Victim, VictimAdmin)
