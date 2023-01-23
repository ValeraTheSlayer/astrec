from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CHOICES = (
        ('OPERATOR', 'ОПЕРАТОР'),
        ('LEAD ENGINEER', 'ВЕДУЩИЙ ИНЖЕНЕР'),
        ('HEAD OF SERVICE', 'НАЧАЛЬНИК СЛУЖБЫ'),
        ('HEAD OF SCPE', 'НАЧАЛЬНИК СКПЭ'),
        ('CONTROLLER', 'КОНТРОЛЕР'),
    )
    position = models.CharField(max_length=30, choices=CHOICES)
