import uuid

from django.db import models
from users.models import UserAccount


class Conversation(models.Model):
    """
    Conversation model representing a chat conversation.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="Новый чат")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    model = models.CharField(max_length=255, default="gpt-3.5-turbo-0613")
    prompt = models.TextField(
        null=True, blank=True, default="You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown. Respond in the language of the request. The assistant is helpful, creative, clever, and very friendly. Ask your questions in Markdown format.")
    maxTokens = models.IntegerField(default=500)
    temperature = models.FloatField(default=0.7)
    topP = models.FloatField(default=1)
    frequencyPenalty = models.FloatField(default=0)
    presencePenalty = models.FloatField(default=0)

    class Meta:
        ordering = ['-updatedAt']

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
    role = models.CharField(max_length=255, default="user")
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-createdAt']

    def __str__(self):
        return f"Message {self.id} - {self.conversation}"
