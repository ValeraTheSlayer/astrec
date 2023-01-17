from django.db import models
from django.contrib.auth.models import User


class Approval(models.Model):
    approving_person = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)  # для отслеживания цепочки согласований

