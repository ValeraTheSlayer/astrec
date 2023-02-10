from django.contrib import admin
from card.models import Card
from approval.models import Approval
from users.models import User


admin.site.register(User)
admin.site.register(Card)
admin.site.register(Approval)

