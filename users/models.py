from django.contrib.auth.models import AbstractUser
from django.db import models

SPECIALIZED_IN_CHOICE = [
    (1, 'Leukemia'),
    (2, 'Lymphama'),
    (3, 'Melanoma'),
    (4, 'Sarcoma'),
    (5, 'Skin Cancer'),
    (6, 'Others'),
]


class SpecializedInChoices(models.Model):
    specialized_in = models.CharField(max_length=300, choices= SPECIALIZED_IN_CHOICE)

    def __str__(self):
        return self.specialized_in


class User(AbstractUser):
    street_address = models.CharField(max_length=100, blank=True, null=True, default='')
    city = models.CharField(max_length=30, blank=True, null=True, default='')
    state = models.CharField(max_length=30, blank=True, null=True, default='')
    zip = models.CharField('Zip Code', max_length=5, blank=True, null=True, default='')
    mobile_num = models.CharField('Mobile Number', max_length=15, blank=True, null=True)
    email = models.EmailField(null=False, unique=True, error_messages={'unique': 'A user with that email already exists.'})
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)


class Volunteer(User):
    work_phone = models.CharField(max_length=15, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    time_spent = models.CharField(max_length=50, blank=True, null=False, default=3)
    specialized_in = models.ManyToManyField(SpecializedInChoices)

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
