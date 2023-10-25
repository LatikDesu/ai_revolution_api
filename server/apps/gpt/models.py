from django.db import models


class ConversationExplainer(models.Model):
    _input = models.TextField()
    _output = models.TextField()

    class Meta:
        db_table = "t_Conversation_explainer"