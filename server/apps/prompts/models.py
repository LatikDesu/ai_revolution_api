from django.db import models
from users.models import UserAccount
import secrets


def generate_secure_random_id():
    min_value = 10 ** 10  # Minimum value of the range (inclusive)
    max_value = 10 ** 11 - 1  # Maximum value of the range (exclusive)
    return secrets.randbelow(max_value - min_value) + min_value


class SystemPrompt(models.Model):
    """
    System Prompts model
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    prompt = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Системная роль"
        verbose_name_plural = "Системные роли"


class UserPrompt(models.Model):
    """
    User Prompts model
    """
    id = models.BigIntegerField(
        primary_key=True, default=generate_secure_random_id, editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Новая роль')
    description = models.TextField(null=True, blank=True)
    prompt = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Пользовательская роль"
        verbose_name_plural = "Пользовательские роли"
