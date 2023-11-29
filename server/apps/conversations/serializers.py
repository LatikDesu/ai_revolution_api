from rest_framework import serializers

from conversations.models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Message serializer.
    """

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'content',
                  'isFromUser', 'inReplyTo', 'createdAt', ]
        read_only_fields = ('id', 'conversation',
                            'isFromUser', 'inReplyTo', 'createdAt', )


class ConversationSerializer(serializers.ModelSerializer):
    """
    Conversation serializer.
    """
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'model', 'prompt', 'tokenLimit',
                  'temperature', 'createdAt', 'updatedAt', 'messages']


class ConversationConfigSerializer(serializers.ModelSerializer):
    """
    Conversation config serializer.
    """
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'model', 'prompt', 'tokenLimit',
                  'temperature']
