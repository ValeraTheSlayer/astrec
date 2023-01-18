from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from .models import Card
from .forms import SubscriberCardForm as CardForm


# rendering main page
def main_page(request):
    return render(request, 'html/index.html')


def card_create(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/success/')
    else:
        form = CardForm(initial={'key': 'value'})

    return render(request, 'card/card_create_form.html', {'form': form})
