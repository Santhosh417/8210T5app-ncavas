from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from events.models import Event, Enrollment
from django.http import HttpResponse
import csv

class VictimExportCsvMixin:
    def export_as_csv(self, request, queryset):
        # Getting only the fields required
        victims = Victim.objects.all().only("id", "first_name", "last_name", "email", "mobile_num", \
                                               "street_address", "city", "state", "zip", "disease_type",
                                               "notes")
        # Specify the header field names
        field_names = ['Victim ID', 'Victim Name', 'Email', 'Phone', 'Address', 'City', 'State', 'ZIP',\
                                 'Disease type', 'Notes']
        response = HttpResponse(content_type='text/csv')
        # Specify the filename
        response['Content-Disposition'] = 'attachment; filename=Victims_report.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for victim in queryset:
            writer.writerow([victim.id, victim.first_name + " " + victim.last_name, victim.email, victim.mobile_num, \
                             victim.street_address, victim.city, victim.state, victim.zip, victim.disease_type,\
                             victim.notes])

        return response

    export_as_csv.short_description = "Export Selected as CSV"

class VolunteerExportCsvMixin:
    def export_as_csv(self, request, queryset):

        volunteers = Volunteer.objects.all().only("id", "first_name", "last_name", "email", "mobile_num", "work_phone",\
            "street_address", "city", "state", "zip", "time_spent", "specialized_in", "comments")
        formatted_field_names = ['Volunteer ID', 'Volunteer Name', 'Email', 'Phone',\
                                 'Work Phone', 'Address', 'City', 'State', 'ZIP', 'Number of working hours per week',\
                                 'Speciality', 'Additional Information']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Volunteers_report.csv'
        writer = csv.writer(response)
        writer.writerow(formatted_field_names)

        def getSpecializations(volunteerId):
            sps = volunteer.specialized_in.through.objects.filter(volunteer_id = volunteerId)
            specializations = ''
            for s in sps:
                for x in SpecializedInChoices.objects.filter(id=s.specializedinchoices_id):
                    specializations += x.specialized_in + ', '
            return specializations

        for volunteer in queryset:
            writer.writerow([volunteer.id, volunteer.first_name + " " + volunteer.last_name, volunteer.email, volunteer.mobile_num, volunteer.work_phone,\
                             volunteer.street_address, volunteer.city, volunteer.state, volunteer.zip, volunteer.time_spent,\
                             getSpecializations(volunteer.id), volunteer.comments])

        return response
    export_as_csv.short_description = "Export Selected as CSV"

class VolunteerAdmin(admin.ModelAdmin, VolunteerExportCsvMixin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'work_phone')
    actions = ["export_as_csv"]

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

    def has_delete_permission(self, request, obj=None):
        full_path = request.get_full_path()
        split = full_path.split("/")
        if len(split) > 5:
            volunteer_id = split[4]
            if(volunteer_id.isnumeric()):
                events = Event.objects.filter(volunteer__id = volunteer_id)
                if len(events) == 0:
                    return True
        else:
            return False

class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'work_phone')
    actions = ["export_as_csv"]

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

class VictimAdmin(admin.ModelAdmin, VictimExportCsvMixin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'disease_type')
    actions = ["export_as_csv"]

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

    def has_delete_permission(self, request, obj=None):
        full_path = request.get_full_path()
        split = full_path.split("/")
        if len(split) > 5:
            victim_id = split[4]
            if(victim_id.isnumeric()):
                enrollments = Enrollment.objects.filter(victim__id = victim_id)
                if len(enrollments) == 0:
                    return True
        else:
            return False

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Victim, VictimAdmin)
admin.site.register(SpecializedInChoices)

