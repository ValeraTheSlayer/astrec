import logging
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View

from .models import Card, DOC_TYPES, CardIndividual, CardLegalEntity
from .forms import SubscriberCardForm as CardForm, CardIndividualForm, \
    CardLegalEntityForm
from .utils import my_view

logger = logging.getLogger(__name__)
entity_map = {'individual': CardIndividual, 'legal': CardLegalEntity}


# rendering main page
@my_view
def main_page(request):
    """
    Главная страница, дашборд и статистика заявок
    """
    # TODO: пока отображает список заявок, в будущем д.б. дашборд
    return render(request, 'html/index.html')


@my_view
def card_list(request, entity='individual'):
    cards = Card.objects.select_related(f'{entity}_entity').filter(is_archived=False, **{f'{entity}_entity__isnull': False})
    return render(request, 'card/card_list.html',
                  {'cards': cards})


@my_view
def card_archive(request):
    cards = Card.objects.filter(is_archived=True)
    return render(request, 'card/card_list.html',
                  {'cards': cards, 'is_individual': True})


@my_view
def card_detail(request, cid, entity='individual'):
    card = Card.objects.select_related(f'{entity}_entity').filter(is_archived=False, **{f'{entity}_entity__isnull': False}).get(**{f'{entity}_entity_id': cid})
    context = {'title': 'Детали карточки', 'card': card, 'is_individual': entity == 'individual'}
    return render(request, 'card/card_detail.html', context=context)


@my_view
def card_create(request):
    if request.method == "POST":
        form = CardForm(request.POST or None)
        link = request.get_full_path()
        is_individual = 'individual' in link
        form_secondary = CardIndividualForm(
            request.POST or None) if is_individual else CardLegalEntityForm(
            request.POST or None)

        if form.is_valid() and form_secondary.is_valid():
            card_secondary_obj = form_secondary.save()
            card_obj = form.save(commit=False)
            card_obj.received_at = datetime.strptime(
                request.POST.get('created_date') + ', ' + request.POST.get(
                    'created_time'), '%Y-%m-%d, %H:%M')
            if is_individual:
                card_obj.individual_entity = card_secondary_obj
            else:
                card_obj.legal_entity = card_secondary_obj
            card_obj.save()
            attachment = request.FILES.get('file')
            if attachment and attachment.name.endswith('.pdf'):
                card_obj.file = attachment
                card_obj.save()
            elif attachment:
                messages.add_message(request, messages.ERROR,
                                     'Загружать можно только файлы формата .PDF')
                return render(request, 'card/card_create_form.html',
                              {'form': form,
                               f'form_{"individual" if is_individual else "legal_entity"}': form_secondary,
                               'is_individual': is_individual})
            messages.add_message(request, messages.SUCCESS,
                                 'Заявка успешно создана!')
            return HttpResponseRedirect(
                f'/cards/{"individual" if is_individual else "legal"}')
        else:
            messages.add_message(request, messages.ERROR,
                                 'При добавлении карточки обнаружены ошибки! Проверьте заполнение.' + str(form.errors))
    else:
        form = CardForm()
        link = request.get_full_path()
        is_individual = 'individual' in link
        form_secondary = CardIndividualForm(
            request.POST or None) if is_individual else CardLegalEntityForm(
            request.POST or None)

    return render(request, 'card/card_create_form.html', {'form': form,
                                                          f'form_{"individual" if is_individual else "legal_entity"}': form_secondary,
                                                          'is_individual': is_individual})


@my_view
def card_statistics(request):
    """
    Функция для создания статистики
    """
    filters = {}
    for param in ['operator', 'power', 'task', 'object_category',
                  'phone_number', 'city', 'district', 'street', 'bldg',
                  'block', 'apt_num', 'floor', 'entrance', 'square',
                  'connection_point', 'nominal', 'main_point',
                  'counter_number',
                  'counter_model', 'contract', 'organization', 'comment',
                  ]:
        if request.GET.get(param, None):
            filters[f'{param}'] = request.GET.get(param)

    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if start_date and end_date:
        filters['created_at__range'] = [start_date, end_date]
    elif start_date:
        filters['created_at__gte'] = start_date
    elif end_date:
        filters['created_at__lte'] = end_date

    cards = Card.objects.filter(**filters)
    district_counts = cards.values('district').annotate(Count('id'))
    district_stats = {}
    for district in district_counts:
        district_stats[district['district']] = district['id__count']

    return JsonResponse({"card_stats_by_district": district_stats})

