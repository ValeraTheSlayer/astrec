from django import forms
from django.db import models
from django.forms import ModelForm, TextInput
from .models import Card


class SubscriberCardForm(ModelForm):
    class Meta:
        model = Card
        # exclude = ['created_at', 'updated_at']
        exclude = ('updated_at',)
        widgets = {
            'comment': TextInput(),
        }