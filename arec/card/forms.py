from django import forms
from django.forms import ModelForm
from .models import Card


class SubscriberCardForm(ModelForm):
    class Meta:
        model = Card
        exclude = ['created_at', 'updated_at']