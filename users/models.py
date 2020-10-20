from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    street_address = models.CharField(max_length=100, null=False, default= '')
    city = models.CharField(max_length=30, null=False, default= '')
    state = models.CharField(max_length=30, null=False, default= '')
    zip = models.CharField(max_length=5, null=False, default= '')
    mobile_num = models.CharField (max_length=15, null=True)

class Volunteer(User):
    work_phone = models.CharField (max_length=15, null=True)
    hours = models.CharField(max_length=2, null=True)
    specialization = models.CharField (max_length=30, null=True)
    notes = models.CharField (max_length=300, null=True, blank=True)
    class Meta:
         verbose_name = "Volunteer"

    def __str__(self):
        return self.username

class Staff(User):
    work_phone = models.CharField (max_length=15, null=True)
    class Meta:
         verbose_name = "Staff"

    def __str__(self):
        return self.username

class Victim(User):
    disease_type = models.CharField (max_length=50, null=True)
    notes = models.CharField (max_length=300, null=True, blank=True)
    class Meta:
         verbose_name = "Victim"

    def __str__(self):
        return self.username
