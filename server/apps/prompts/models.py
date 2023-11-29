from django.db import models


class SystemPrompt(models.Model):
    """
    System Prompts model
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    prompt = models.TextField()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Системный промпт"
        verbose_name_plural = "Системные промпты"
