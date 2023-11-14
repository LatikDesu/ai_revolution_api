from rest_framework import serializers

from prompts.models import SystemPrompt, UserPrompt


class SystemPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemPrompt
        fields = ('id', 'title', 'description', 'prompt')
        read_only_fields = ('id', 'title', 'description', 'prompt')


class UserPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPrompt
        fields = ('id', 'title', 'description', 'prompt')
        read_only_fields = ('id',)

    def create(self, validated_data):
        return UserPrompt.objects.create(**validated_data)
