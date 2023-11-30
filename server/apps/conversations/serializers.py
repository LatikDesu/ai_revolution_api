from rest_framework import serializers

from conversations.models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Message serializer.
    """
    stream = serializers.BooleanField(
        default=True, required=False)

    def create(self, validated_data):
        stream = validated_data.pop('stream', None)

        return Message.objects.create(**validated_data)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'content',
                  'isFromUser', 'inReplyTo', 'createdAt', 'stream',]
        read_only_fields = ('id', 'conversation',
                            'isFromUser', 'inReplyTo', 'createdAt', )
        extra_kwargs = {
            'stream': {'write_only': True},
        }


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
