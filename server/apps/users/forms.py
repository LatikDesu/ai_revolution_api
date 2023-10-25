from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserAccount


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserAccount
        fields = ('email','first_name', 'last_name')  


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name')  