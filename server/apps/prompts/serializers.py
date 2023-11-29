from rest_framework import serializers

from prompts.models import SystemPrompt


class SystemPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemPrompt
        fields = ('id', 'title', 'description', 'prompt')
        read_only_fields = ('id', 'title', 'description', 'prompt')
