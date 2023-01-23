import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import View

from .models import Card
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
def card_create(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Заявка успешно создана!')
            return HttpResponseRedirect('/cards/')
        else:
            logger.debug(form.errors)
            messages.add_message(request, messages.ERROR, 'При добавлении карточки обнаружены ошибки!'
                                                          'Проверьте заполнение.')
    else:
        form = CardForm()

    return render(request, 'card/card_create_form.html', {'form': form})
