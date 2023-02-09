from django.db import models

from users.models import User


class Approval(models.Model):
    approved_at = models.DateTimeField(auto_now=True)
    remark = models.TextField(blank=True)  # для каких-либо комментариев/пометок на этапе согласования

    card_ref = models.ForeignKey('card.Card', on_delete=models.CASCADE)
    approving_person = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)  # для отслеживания цепочки согласований

