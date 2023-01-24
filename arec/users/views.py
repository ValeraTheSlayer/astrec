from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CreationForm, UserAuthenticationForm


class CustomLoginView(LoginView):
    authentication_form = UserAuthenticationForm
    template_name = 'users/loggin.html'


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('card_list')
    template_name = 'users/signup.html'
