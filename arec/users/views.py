from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, reverse

from .forms import CreationForm, UserAuthenticationForm, ProfileForm


class CustomLoginView(LoginView):
    authentication_form = UserAuthenticationForm
    template_name = 'users/loggin.html'


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('index')
    template_name = 'users/signup.html'


class LogoutView(TemplateView):
    template_name = "users/signup.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Вы вышли из ситемы!')
        return redirect(reverse('index'))


def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form})
