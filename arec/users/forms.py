from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'position',)


class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
