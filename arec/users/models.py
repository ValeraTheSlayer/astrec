from django.db import models
from django.contrib.auth.models import AbstractUser
from arec.settings import AREC_POSITIONS, AREC_DISTRICTS


class User(AbstractUser):
    position = models.CharField(max_length=30, choices=AREC_POSITIONS)
    district = models.CharField(max_length=30, choices=AREC_DISTRICTS, null=True)

