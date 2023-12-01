from rest_framework import serializers

from conversations.models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Message serializer.
    """

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'content',
                  'role', 'createdAt',]
        read_only_fields = ('id', 'createdAt', )


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
