import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View

from .models import Card, DocScan, DOC_TYPES
from .forms import SubscriberCardForm as CardForm
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
    cards = Card.objects.all()
    return render(request, 'card/card_list.html',
                  {'cards': cards})

@my_view
def card_detail(request, cid):
    card = Card.objects.get(pk=cid)
    scans = DocScan.objects.all().filter(card_id=cid)
    context = {'title': 'Детали карточки', 'card': card, 'scans': scans}
    return render(request, 'card/card_detail.html', context=context)

@my_view
def card_create(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card_obj = form.save()
            for doc in DOC_TYPES:
                doc_type = doc[0]
                logger.debug(request.FILES)
                attachment = request.FILES.get(doc_type, None)
                if attachment is not None:
                    logger.debug(f'attached file {doc_type} detected, path {attachment}')
                    scan = DocScan(doc_file=attachment,
                                   doctype=doc_type,
                                   card=card_obj)
                    scan.save()
            messages.add_message(request, messages.SUCCESS, 'Заявка успешно создана!')
            return HttpResponseRedirect('/cards/')
        else:
            logger.debug(f'invalid form {form.errors}')
            messages.add_message(request, messages.ERROR, 'При добавлении карточки обнаружены ошибки! '
                                                          'Проверьте заполнение.')
    else:
        form = CardForm()
    doc_types = [{'name': v[0], 'label': v[1]} for v in DOC_TYPES]
    return render(request, 'card/card_create_form.html', {'form': form, 'doc_types': doc_types})
