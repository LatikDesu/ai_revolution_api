from rest_framework import serializers
from gpt.models import ConversationExplainer
from gpt.utils import send_request_to_gpt

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationExplainer
        fields = ("id","_input","_output")
        extra_kwargs = {
            "_output":{"read_only":True}
        }
    
    def create(self, validated_data):
        ce = ConversationExplainer(**validated_data)
        _output = send_request_to_gpt(validated_data["_input"])
        ce._output = _output
        ce.save()
        return ce