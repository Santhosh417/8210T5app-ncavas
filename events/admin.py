from django.contrib import admin
from .models import Location, Event, Enrollment


class EnrollmentInline(admin.TabularInline):
    model = Enrollment

class ActivityAdmin(admin.ModelAdmin):
    inlines = [
        EnrollmentInline,
    ]

admin.site.register(Location)
admin.site.register(Event, ActivityAdmin)
