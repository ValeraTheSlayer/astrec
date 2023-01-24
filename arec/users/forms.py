from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'position',)


class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Введите имя пользователя'
        self.fields['password'].label = 'Введите пароль'

    class Meta:
        model = User
        fields = ('username', 'password')

