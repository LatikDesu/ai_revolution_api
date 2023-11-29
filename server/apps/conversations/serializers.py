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
        read_only_fields = ('id', 'conversation',
                            'is_from_user', 'in_reply_to', 'created_at', )


class ConversationSerializer(serializers.ModelSerializer):
    """
    Conversation serializer.
    """
    messages = MessageSerializer(many=True, read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'model', 'prompt', 'tokenLimit',
                  'maxLength', 'temperature', 'created_at', 'updated_at', 'messages', 'folder']

    def get_created_at(self, obj):
        created_at = obj.get('created_at') if isinstance(
            obj, dict) else obj.created_at
        return time_since(created_at)


class ConversationConfigSerializer(serializers.ModelSerializer):
    """
    Conversation config serializer.
    """
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'model', 'prompt', 'tokenLimit',
                  'maxLength', 'temperature', 'folder']


class FolderConversationSerializer(serializers.ModelSerializer):
    """
    Folder conversation serializer.
    """
    title = serializers.CharField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at']
        ordering = ['-created_at']


class FolderSerializer(serializers.ModelSerializer):
    """
    Folder serializer.
    """
    conversations = FolderConversationSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'title', 'conversations']
