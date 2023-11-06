from rest_framework import serializers

from conversations.models import Conversation, Folder, Message
from conversations.utils import time_since


class MessageSerializer(serializers.ModelSerializer):
    """
    Message serializer.
    """

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'content',
                  'is_from_user', 'in_reply_to', 'created_at', ]


class ConversationSerializer(serializers.ModelSerializer):
    """
    Conversation serializer.
    """
    messages = MessageSerializer(many=True, read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'favourite',
                  'archive', 'created_at', 'messages', 'folder']

    def get_created_at(self, obj):
        return time_since(obj.created_at)


class FolderConversationSerializer(serializers.ModelSerializer):
    """
    Folder conversation serializer.
    """
    id = serializers.IntegerField()
    title = serializers.CharField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at']
        ordering = ['-created_at']


class FolderSerializer(serializers.ModelSerializer):
    """
    Folder serializer.
    """
    conversation = ConversationSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'title', 'conversation']
