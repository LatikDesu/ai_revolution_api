import uuid

from django.db import models
from users.models import UserAccount


class Folder(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="Новая папка")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Conversation(models.Model):
    """
    Conversation model representing a chat conversation.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="Новый чат")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    folder = models.ForeignKey(
        Folder, null=True, blank=True, on_delete=models.SET_NULL, related_name='conversations')

    model = models.CharField(max_length=255, default="GPT-35")
    prompt = models.TextField(
        null=True, blank=True, default="You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown. Respond in the language of the request")
    tokenLimit = models.IntegerField(default=1000)
    maxLength = models.IntegerField(default=10000)
    temperature = models.FloatField(default=0.7)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Conversation {self.title} - {self.user.username}"


class Message(models.Model):
    """
    Message model representing a message within a conversation.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
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
