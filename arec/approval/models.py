from django.db import models
from arec.settings import AREC_POSITIONS
from users.models import User


class Approval(models.Model):
    approved_at = models.DateTimeField(auto_now=True)
    remark = models.TextField(blank=True)  # для каких-либо комментариев/пометок на этапе согласования
    card_ref = models.ForeignKey('card.Card', on_delete=models.CASCADE)
    approving_person = models.ForeignKey(User, on_delete=models.CASCADE)

    # it is a separate field since it shouldn't be as permanent ref to the approving_person.position
    # to be able to have various approving with the same user -> easier demonstration of the approval-flow
    approving_position = models.CharField(max_length=30,
                                          choices=AREC_POSITIONS,
                                          null=False, blank=False, default=AREC_POSITIONS[0][0])

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)  # для отслеживания цепочки согласований

