from django.db import models

from users.models import User


class Approval(models.Model):
    approving_person = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_at = models.DateTimeField(auto_now=True)
    remark = models.TextField(blank=True)  # для каких-либо комментариев/пометок на этапе согласования
    parent = models.ForeignKey('self', on_delete=models.CASCADE)  # для отслеживания цепочки согласований

