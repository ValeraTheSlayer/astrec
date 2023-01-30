import logging
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View

from .models import Card, DOC_TYPES, CardIndividual
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
def card_list(request):
    link = request.get_full_path()
    is_individual = 'individual' in link
    if is_individual:
        cards = CardIndividual.objects.select_related('card').all()
    else:
        cards = CardLegalEntity.objects.select_related('card').all()
    return render(request, 'card/card_list.html',
                  {'cards': cards, 'is_individual': is_individual})


@my_view
def card_detail(request, cid):
    link = request.get_full_path()
    is_individual = 'individual' in link
    if is_individual:
        card = CardIndividual.objects.select_related('card').get(pk=cid)
    else:
        card = CardLegalEntity.objects.select_related('card').get(pk=cid)
    context = {'title': 'Детали карточки', 'card': card}
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
            if is_individual:
                card_obj.created_at = datetime.strptime(
                    request.POST.get('created_date') + ', ' + request.POST.get(
                        'created_time'), '%Y-%m-%d, %H:%M')
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
                f'/cards/{"individuals" if is_individual else "legal-entities"}')
        else:
            messages.add_message(request, messages.ERROR,
                                 'При добавлении карточки обнаружены ошибки! Проверьте заполнение.')
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

