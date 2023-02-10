from random import choices

import django_filters
from django.forms import TextInput, Select
from django_filters import DateFilter, CharFilter, ChoiceFilter

from .models import *
from arec.settings import AREC_DISTRICTS


class CardFilter(django_filters.FilterSet):
    operator = CharFilter(field_name='operator', lookup_expr='icontains',
                          label='Оператор', widget=TextInput(attrs= {'style': 'width:100px;'}))
    district = ChoiceFilter(field_name='district', label='Район',
                            choices=AREC_DISTRICTS, widget=Select(attrs={'style': 'width:100px;'}))
    individual_entity__iin = CharFilter(field_name='individual_entity__iin',
                                        lookup_expr='icontains', label='ИИН')
    legal_entity__bin = CharFilter(field_name='legal_entity__bin',
                                   lookup_expr='icontains', label='БИН')
    city = CharFilter(field_name='city', lookup_expr='icontains',
                      label='Город')
    street = CharFilter(field_name='street', lookup_expr='icontains',
                        label='Улица')
    object_category = ChoiceFilter(field_name='object_category',
                                 label='Категория объекта', choices=OBJECT_CATEGORY, widget=Select(attrs={'style': 'width:100px;'}))
    task = CharFilter(field_name='task', lookup_expr='icontains',
                      label='Задача')
    bldg = CharFilter(field_name='bldg', label='Номер дома')
    block = CharFilter(field_name='block', label='Блок')
    apt_num = CharFilter(field_name='apt_num', label='Номер квартиры')
    floor = CharFilter(field_name='floor', label='Этаж')
    entrance = CharFilter(field_name='entrance', label='Подъезд')

    class Meta:
        model = Card
        fields = ('district', 'individual_entity__iin', 'legal_entity__bin',
                  'city', 'street', 'bldg',
                  'block', 'apt_num', 'floor', 'entrance', 'operator',
                  'object_category',
                  'task',)
