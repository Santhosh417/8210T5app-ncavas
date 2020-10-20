from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, null=False)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="customer")
    UNMARRIED = 'UM'
    MARRIED = 'MA'
    BLANK = ''
    marital_status_choices = (
        (BLANK,''),
        (UNMARRIED, 'Unmarried'),
        (MARRIED, 'Married'),
    )
    marital_status = models.CharField(max_length=2,
                                      choices=marital_status_choices,
                                      default=BLANK)
    vacation_preference_choices = (
        ('Beach','Beach'),
        ('Nature', 'Nature'),
        ('Adventure', 'Adventure'),
        ('Inspiring', 'Inspiring'),
    )
    preferred_type_of_vacations = models.CharField(max_length=1, choices=vacation_preference_choices)

    def __str__(self):
        return self.user.username



