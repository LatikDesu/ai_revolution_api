from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import UserAccount


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserAccount
        fields = ("email", "username", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserAccount
        fields = ("first_name", "last_name", "username")
