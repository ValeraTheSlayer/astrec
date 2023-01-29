import logging
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View

from .models import Card, DocScan, DOC_TYPES, CardIndividual
from .forms import SubscriberCardForm as CardForm, CardIndividualForm, \
    CardLegalEntity, CardLegalEntityForm
from .utils import my_view

logger = logging.getLogger(__name__)


# rendering main page
@my_view
def main_page(request):
    """
    Главная страница, дашборд и статистика заявок
    """
    # TODO: пока отображает список заявок, в будущем д.б. дашборд
    return render(request, 'html/index.html')


@my_view
def card_list_individuals(request):
    cards = CardIndividual.objects.select_related('card').all()
    return render(request, 'card/card_list_individuals.html',
                  {'cards': cards})

@my_view
def card_detail_individual(request, cid):
    card = CardIndividual.objects.select_related('card').get(pk=cid)
    scans = DocScan.objects.all().filter(card_id=cid)
    context = {'title': 'Детали карточки', 'card': card, 'scans': scans}
    return render(request, 'card/card_detail_individuals.html', context=context)

@my_view
def card_list_legal_entities(request):
    cards = CardLegalEntity.objects.select_related('card').all()
    return render(request, 'card/card_list_legal_entities.html',
                  {'cards': cards})

@my_view
def card_detail_legal_entity(request, cid):
    card = CardLegalEntity.objects.select_related('card').get(pk=cid)
    scans = DocScan.objects.all().filter(card_id=cid)
    context = {'title': 'Детали карточки', 'card': card, 'scans': scans}
    return render(request, 'card/card_detail_legal_entities.html', context=context)

@my_view
def card_create_individual(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        form_individual = CardIndividualForm(request.POST)
        print('created date', form)
        if form.is_valid() and form_individual.is_valid():
            card_individual_obj = form_individual.save()
            card_obj = form.save(commit=False)
            card_obj.created_at = datetime.strptime(request.POST.get('created_date')
                                                    + ', '
                                                    + request.POST.get('created_time'),
                                                    '%Y-%m-%d, %H:%M')
            card_obj.individual_entity = card_individual_obj
            card_obj.save()
            for doc in DOC_TYPES:
                doc_type = doc[0]
                logger.debug(request.FILES)
                attachment = request.FILES.get(doc_type, None)
                if attachment is not None:
                    logger.debug(
                        f'attached file {doc_type} detected, path {attachment}')
                    scan = DocScan(doc_file=attachment,
                                   doctype=doc_type,
                                   card=card_obj)
                    scan.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Заявка успешно создана!')
            return HttpResponseRedirect('/cards/individuals')
        else:
            logger.debug(f'invalid form {form.errors}')
            messages.add_message(request, messages.ERROR,
                                 'При добавлении карточки обнаружены ошибки! '
                                 'Проверьте заполнение.')
    else:
        form = CardForm()
        form_individual = CardIndividualForm()
    doc_types = [{'name': v[0], 'label': v[1]} for v in DOC_TYPES]
    return render(request, 'card/card_individual_create_form.html',
                  {'form': form, 'form_individual': form_individual,
                   'doc_types': doc_types})

@my_view
def card_create_legal_entity(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        form_legal_entity = CardLegalEntityForm(request.POST)
        if form.is_valid() and form_legal_entity.is_valid():
            card_legal_entity_obj = form_legal_entity.save()
            card_obj = form.save(commit=False)
            card_obj.legal_entity = card_legal_entity_obj
            card_obj.save()
            for doc in DOC_TYPES:
                doc_type = doc[0]
                logger.debug(request.FILES)
                attachment = request.FILES.get(doc_type, None)
                if attachment is not None:
                    logger.debug(
                        f'attached file {doc_type} detected, path {attachment}')
                    scan = DocScan(doc_file=attachment,
                                   doctype=doc_type,
                                   card=card_obj)
                    scan.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Заявка успешно создана!')
            return HttpResponseRedirect('/cards/legal-entities')
        else:
            logger.debug(f'invalid form {form.errors}')
            messages.add_message(request, messages.ERROR,
                                 'При добавлении карточки обнаружены ошибки! '
                                 'Проверьте заполнение.')
    else:
        form = CardForm()
        form_legal_entity = CardLegalEntityForm()
    doc_types = [{'name': v[0], 'label': v[1]} for v in DOC_TYPES]
    return render(request, 'card/card_legal_entity_create_form.html',
                  {'form': form, 'form_legal_entity': form_legal_entity,
                   'doc_types': doc_types})



