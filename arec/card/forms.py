from django import forms
from django.db import models
from django.forms import ModelForm, TextInput
from .models import Card, CardIndividual, CardLegalEntity


class SubscriberCardForm(ModelForm):
    class Meta:
        model = Card
        # exclude = ['created_at', 'updated_at']
        exclude = ('updated_at',)
        widgets = {
            'comment': TextInput(),
        }


class CardIndividualForm(forms.ModelForm):
    class Meta:
        model = CardIndividual
        fields = '__all__'


class CardLegalEntityForm(forms.ModelForm):
    class Meta:
        model = CardLegalEntity
        fields = '__all__'
