from rest_framework import serializers
from conversations.models import ConversationFlow, Conversation
from conversations.utils import send_request_to_gpt


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('id', 'user', 'timestamp', 'title')
        read_only_fields = ('id', 'user', 'timestamp')

    def create(self, validated_data):
        return Conversation.objects.create(**validated_data)


class ConversationFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationFlow
        fields = ("id", "conversation", "_input", "_output")
        extra_kwargs = {
            "_output": {"read_only": True}
        }

    def create(self, validated_data):
        ce = ConversationFlow(**validated_data)
        _output = send_request_to_gpt(validated_data["_input"])
        ce._output = _output
        ce.save()
        return ce
