from django.db import models

from users.models import UserAccount


class Conversation(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)


class ConversationFlow(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    _input = models.TextField()
    _output = models.TextField()

    class Meta:
        db_table = "t_Conversation_flow"
