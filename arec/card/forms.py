from django import forms
from django.db import models
from django.forms import ModelForm, TextInput
from .models import Card, CardIndividual, CardLegalEntity


class SubscriberCardForm(ModelForm):
    created_date = forms.DateField()
    created_time = forms.TimeField()

    class Meta:
        model = Card
        exclude = ('received_at', 'updated_at', 'created_at', 'last_approval')
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
