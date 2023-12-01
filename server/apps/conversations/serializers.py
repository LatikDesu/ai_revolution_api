from rest_framework import serializers

from conversations.models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Message serializer.
    """

    def validate_role(self, value):
        if value not in ['user', 'assistant']:
            raise serializers.ValidationError('Invalid role type')
        return value

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'content',
                  'role', 'createdAt',]
        read_only_fields = ('id', 'conversation', 'createdAt', )


class ConversationListSerializer(serializers.ModelSerializer):
    """
    Conversation list serializer.
    """

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'createdAt', 'updatedAt']
        ordering = ('updatedAt')


class ConversationSerializer(serializers.ModelSerializer):
    """
    Conversation serializer.
    """
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'model', 'prompt', 'maxTokens',
                  'temperature', 'topP', 'frequencyPenalty', 'presencePenalty',  'createdAt', 'updatedAt', 'messages']


class ConversationConfigSerializer(serializers.ModelSerializer):
    """
    Conversation config serializer.
    """
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'model', 'prompt', 'maxTokens',
                  'temperature', 'topP', 'frequencyPenalty', 'presencePenalty',]
