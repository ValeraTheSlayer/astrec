from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    POSITIONS = (
        ('OPERATOR', 'ОПЕРАТОР'),
        ('LEAD_ENGINEER', 'ВЕДУЩИЙ ИНЖЕНЕР'),
        ('HEAD_SERVICE', 'НАЧАЛЬНИК СЛУЖБЫ'),
        ('HEAD_SCPE', 'НАЧАЛЬНИК СКПЭ'),
        ('CONTROLLER', 'КОНТРОЛЛЕР'),
    )
    position = models.CharField(max_length=30, choices=POSITIONS, verbose_name='Должность')
