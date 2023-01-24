from django.contrib.auth import views
from django.urls import path, reverse_lazy

from .apps import UsersConfig
from .views import SignUp, CustomLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('signup/', SignUp.as_view(template_name='signup.html'),
         name='signup'),
    path(
        'logout/',
        views.LogoutView.as_view(template_name='logged_out.html'),
        name='logout',
    ),
    path(
        'login/',
        CustomLoginView.as_view(template_name='loggin.html'),
        name='login',
    ),
]