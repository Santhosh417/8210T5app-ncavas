from django.db import models
from users.models import Staff, Volunteer, Victim

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=26, null=True)
    city = models.CharField(max_length=26, null=True)
    state = models.CharField(max_length=26, null=True)
    zip = models.CharField(max_length=6, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50, null=True)
    event_choices = (
        ('Public','Public'),
        ('OneToOne', 'One To One'),
        ('Group', 'Group')
    )
    event_type = models.CharField(max_length=10, choices=event_choices)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    description = models.CharField(max_length=300, null=True, blank=True)
    is_important = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, related_name='event_staff')
    volunteer = models.ForeignKey(Volunteer, on_delete=models.DO_NOTHING, related_name='event_volunteer')
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='event_location')

    def __str__(self):
        return self.event_name


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING,
                              related_name='enrollment_event')
    victim = models.ForeignKey(Victim, on_delete=models.DO_NOTHING,
                                  related_name='enrollment_victim')
    notes = models.CharField(max_length=300, null=True, blank=True)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return self.victim.first_name
