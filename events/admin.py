from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from .models import Location, Event, Enrollment
from django.http import HttpResponse
import csv


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        formatted_field_names = []
        for name in field_names:
            if 'img' in name:
                field_names.remove(name)
                continue
            else:
                field_name = ""
                for n in name.split('_'):
                    n = n[0].upper() + n[1:]
                    field_name += n + " "
                formatted_field_names.append(field_name.rstrip())
        response = HttpResponse(content_type='text/csv')
        if str(meta) == "events.event":
            meta = "Events_report"
        elif str(meta) == "events.enrollment":
            meta = "Enrollments_report"
        else:
            meta = "Locations_report"
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(formatted_field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class EnrollmentAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display =('event_name', 'event_date', 'victim_name', 'notes', 'is_important')
    #adding the export functionality to this list make it visible in the actions dropdown on the admin panel.
    actions = ["export_as_csv"]

    def event_name(self, instance):
        try:
            return instance.event.event_name
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def event_date(self, instance):
        try:
            return instance.event.start_date_time.strftime("%A, %d %b %Y %H %M") + " to " + instance.event.end_date_time.strftime("%A, %d %b %Y %H %M")
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

class ActivityAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ("event_name", "event_date")
    actions = ["export_as_csv"]

    def event_date(self, instance):
        try:
            return instance.start_date_time.strftime("%A, %d %b %Y %H %M") + " to " + instance.end_date_time.strftime("%A, %d %b %Y %H %M")
        except ObjectDoesNotExist:
            return 'ERROR!!'

    inlines = [
        EnrollmentInline,
    ]

class LocationAdmin(admin.ModelAdmin, ExportCsvMixin):
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
