from django.contrib.auth import views, logout
from django.urls import path, reverse_lazy

from .apps import UsersConfig
from .views import SignUp, CustomLoginView, LogoutView, profile

app_name = UsersConfig.name

urlpatterns = [
    path('signup/', SignUp.as_view(template_name='signup.html'),
         name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'login/',
        CustomLoginView.as_view(template_name='loggin.html'),
        name='login',
    ),
    path('profile/', profile, name='profile'),
]