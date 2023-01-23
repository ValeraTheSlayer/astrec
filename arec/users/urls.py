from django.contrib.auth import views
from django.urls import path, reverse_lazy

from .apps import UsersConfig
from .views import SignUp

app_name = UsersConfig.name

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path(
        'logout/',
        views.LogoutView.as_view(template_name='logged_out.html'),
        name='logout',
    ),
    path(
        'login/',
        views.LoginView.as_view(template_name='login.html'),
        name='login',
    ),
]