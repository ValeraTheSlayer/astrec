from random import choices

import django_filters
from django.forms import TextInput, Select
from django_filters import DateFilter, CharFilter, ChoiceFilter

from .models import *
from arec.settings import AREC_DISTRICTS


class CardFilter(django_filters.FilterSet):
    operator = CharFilter(
        field_name='operator',
        lookup_expr='icontains',
        label='Оператор',
        widget=TextInput(attrs={'style': 'width:100px;'})
    )
    district = ChoiceFilter(
        field_name='district',
        label='Район',
        choices=AREC_DISTRICTS,
        widget=Select(attrs={'style': 'width:100px;'})
    )
    individual_entity__iin = CharFilter(
        field_name='individual_entity__iin',
        lookup_expr='icontains',
        label='ИИН',
        widget=TextInput(attrs={'style': 'width:110px;'})
    )
    individual_entity__first_name = CharFilter(
        field_name='individual_entity__first_name',
        lookup_expr='icontains',
        label='Имя',
        widget=TextInput(attrs={'style': 'width:100px;'})
    )
    individual_entity__last_name = CharFilter(
        field_name='individual_entity__last_name',
        lookup_expr='icontains',
        label='Фамилия',
        widget=TextInput(attrs={'style': 'width:100px;'})
    )
    individual_entity__patronymic_name = CharFilter(
        field_name='individual_entity__patronymic_name',
        lookup_expr='icontains',
        label='Отчество',
        widget=TextInput(attrs={'style': 'width:100px;'})
    )
    legal_entity__bin = CharFilter(
        field_name='legal_entity__bin',
        lookup_expr='icontains',
        label='БИН',
        widget=TextInput(attrs={'style': 'width:110px;'})
    )
    legal_entity__company_name = CharFilter(
        field_name='legal_entity__company_name',
        lookup_expr='icontains', label='Название компании',
        widget=TextInput(attrs={'style': 'width:100px;'}))
    phone_number = CharFilter(
        field_name='phone_number',
        label='Телефон',
        widget=TextInput(attrs={'style': 'width:110px;'})
    )
    city = CharFilter(
        field_name='city',
        lookup_expr='icontains',
        label='Город',
        widget=TextInput(attrs={'style': 'width:100px;'})
    )
    street = CharFilter(
        field_name='street',
        lookup_expr='icontains',
        label='Улица',
        widget=TextInput(attrs={'style': 'width:100px;'})
    )
    object_category = ChoiceFilter(
        field_name='object_category',
        label='Категория объекта',
        choices=OBJECT_CATEGORY,
        widget=Select(attrs={'style': 'width:100px;'})
    )
    task = ChoiceFilter(
        field_name='task',
        label='Задача',
        choices=TASK,
        widget=Select(attrs={'style': 'width:100px;'})
    )
    bldg = CharFilter(
        field_name='bldg',
        label='Номер дома',
        widget=TextInput(attrs={'style': 'width:50px;'})
    )
    block = CharFilter(
        field_name='block',
        label='Блок',
        widget=TextInput(attrs={'style': 'width:50px;'})
    )
    apt_num = CharFilter(
        field_name='apt_num',
        label='Номер квартиры',
        widget=TextInput(attrs={'style': 'width:50px;'})
    )
    floor = CharFilter(
        field_name='floor',
        label='Этаж',
        widget=TextInput(attrs={'style': 'width:50px;'})
    )
    entrance = CharFilter(
        field_name='entrance',
        label='Подъезд',
        widget=TextInput(attrs={'style': 'width:50px;'})
    )

    class Meta:
        model = Card
        fields = ('district',
                  'individual_entity__iin',
                  'individual_entity__first_name',
                  'individual_entity__last_name',
                  'individual_entity__patronymic_name',
                  'legal_entity__bin',
                  'legal_entity__company_name',
                  'city',
                  'street',
                  'bldg',
                  'block',
                  'apt_num',
                  'floor',
                  'entrance',
                  'operator',
                  'object_category',
                  'task',
                  'phone_number')
