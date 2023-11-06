from django.db import models
import secrets

from users.models import UserAccount


def generate_secure_random_id():
    min_value = 10 ** 10  # Minimum value of the range (inclusive)
    max_value = 10 ** 11 - 1  # Maximum value of the range (exclusive)
    return secrets.randbelow(max_value - min_value) + min_value


class Folder(models.Model):
    id = models.BigIntegerField(
        primary_key=True, default=generate_secure_random_id, editable=False)
    title = models.CharField(max_length=255, default="Новая папка")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)


class Conversation(models.Model):
    """
    Conversation model representing a chat conversation.
    """
    id = models.BigIntegerField(
        primary_key=True, default=generate_secure_random_id, editable=False)
    title = models.CharField(max_length=255, default="Новый чат")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    folder = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='folders')

    favourite = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Conversation {self.title} - {self.user.username}"


class Message(models.Model):
    """
    Message model representing a message within a conversation.
    """
    id = models.BigIntegerField(
        primary_key=True, default=generate_secure_random_id, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_from_user = models.BooleanField(default=True)
    in_reply_to = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message {self.id} - {self.conversation}"
