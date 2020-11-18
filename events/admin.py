from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Location, Event, Enrollment
from django.http import HttpResponse, HttpResponseRedirect
import csv
from django.core.mail import send_mail
from django.conf import settings
from datetime import date


class LocationExportCsvMixin:
    def export_as_csv(self, request, queryset):
        # Specify the header field names
        field_names = ['Location Id', 'Location Name', 'Address', 'City', 'State', 'Zip']
        response = HttpResponse(content_type='text/csv')
        # Specify the filename
        response['Content-Disposition'] = 'attachment; filename=Locations_report.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for location in queryset:
            writer.writerow(
                [location.location_id, location.name, location.address, location.city, location.state, location.zip])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class EventExportCsvMixin:
    def export_as_csv(self, request, queryset):
        # Specify the header field names
        field_names = ['Event Id', 'Event Name', 'Event Type', 'Start Date and Time', 'End Date and Time',
                       'Description', \
                       'Staff Name', 'Volunteer Name', 'Location', 'Is important?']
        response = HttpResponse(content_type='text/csv')
        # Specify the filename
        response['Content-Disposition'] = 'attachment; filename=Events_report.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for event in queryset:
            writer.writerow([event.event_id, event.event_name, event.event_type, \
                             event.start_date_time.strftime("%A, %d %b %Y %H:%M"), \
                             event.end_date_time.strftime("%A, %d %b %Y %H:%M"), event.description, \
                             event.staff.first_name + " " + event.staff.last_name, \
                             event.volunteer.first_name + " " + event.volunteer.last_name, \
                             event.location.address + ", " + \
                             event.location.city + ", " + event.location.state + ", " + event.location.zip, \
                             "Yes" if event.is_important else "No"])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class EnrollmentExportCsvMixin:
    def export_as_csv(self, request, queryset):
        # Specify the header field names
        field_names = ['Enrollment Id', 'Event Name', 'Victim Name', 'Notes taken by (volunteer name)', 'Notes', \
                       'Action required?']
        response = HttpResponse(content_type='text/csv')
        # Specify the filename
        response['Content-Disposition'] = 'attachment; filename=Enrollments_report.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for enrollment in queryset:
            writer.writerow([enrollment.enrollment_id, enrollment.event.event_name, \
                             enrollment.victim.first_name + " " + enrollment.victim.last_name, \
                             enrollment.event.volunteer.first_name + " " + enrollment.event.volunteer.last_name, \
                             enrollment.notes, "Yes" if enrollment.is_important else "No"])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class EnrollmentAdmin(admin.ModelAdmin, EnrollmentExportCsvMixin):
    list_display = ('event_name', 'event_date', 'victim_name', 'notes', 'is_important')
    # adding the export functionality to this list make it visible in the actions dropdown on the admin panel.
    actions = ["export_as_csv"]

    def event_name(self, instance):
        try:
            return instance.event.event_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def event_date(self, instance):
        try:
            return instance.event.start_date_time.strftime(
                "%A, %d %b %Y %H:%M") + " to " + instance.event.end_date_time.strftime("%A, %d %b %Y %H:%M")
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def victim_name(self, instance):
        try:
            return instance.victim.first_name + " " + instance.victim.last_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def action_requried(self, instance):
        try:
            return "Yes" if instance.is_important else "No"
        except ObjectDoesNotExist:
            return 'ERROR!!'


class EnrollmentInline(admin.TabularInline):
    model = Enrollment


class ActivityAdmin(admin.ModelAdmin, EventExportCsvMixin):
    list_display = ("event_name", "event_date")
    actions = ["export_as_csv"]
    change_form_template = "event_admin.html"

    def response_change(self, request, obj):
        if "_send-reminder" in request.POST:
            emails = []
            enrollments = Enrollment.objects.filter(event__event_name=obj).exclude(
                event__start_date_time__date__lt=date.today())
            if len(enrollments) == 0:
                messages.error(request, "Event completed already. Cannot send reminders")
            else:
                for enrollment in enrollments:
                    emails.append(enrollment.victim.email)
                    emails.append(enrollment.event.volunteer.email)
                startDate = enrollments[0].event.start_date_time
                body = ('''Hello,

This email is a reminder for an upcoming meeting you have on ''' + str(enrollments[0].event.start_date_time.strftime("%m/%d/%Y, %H:%M")) +
'''. Please contact NCA email for futher details.

Thanks
NCA Team
                        ''')
                send_mail(
                    obj,
                    body,
                    settings.EMAIL_HOST_USER,
                    emails,
                    fail_silently=True,
                )
                self.message_user(request, "Reminder emails sent")

            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    def event_date(self, instance):
        try:
            return instance.start_date_time.strftime("%A, %d %b %Y %H:%M") + " to " + instance.end_date_time.strftime(
                "%A, %d %b %Y %H:%M")
        except ObjectDoesNotExist:
            return 'ERROR!!'

    inlines = [
        EnrollmentInline,
    ]


class LocationAdmin(admin.ModelAdmin, LocationExportCsvMixin):
    list_display = ("location_name", "full_address")
    actions = ["export_as_csv"]

    def location_name(self, instance):
        try:
            return instance.name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def full_address(self, instance):
        try:
            return instance.address + ", " + instance.city + ", " + instance.state + ", " + str(instance.zip)
        except ObjectDoesNotExist:
            return 'ERROR!!'


admin.site.register(Location, LocationAdmin)
admin.site.register(Event, ActivityAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
