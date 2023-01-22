import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from .models import Card
from .forms import SubscriberCardForm as CardForm


logger = logging.getLogger(__name__)


# rendering main page
def main_page(request):
    """
    Главная страница, дашборд и статистика заявок
    """
    # TODO: пока отображает список заявок, в будущем д.б. дашборд
    return render(request, 'html/index.html')


def card_list(request):
    return render(request, 'html/index.html')


def card_create(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cards/')
        else:
            logger.debug(form.errors)
    else:
        form = CardForm()

    return render(request, 'card/card_create_form.html', {'form': form})
