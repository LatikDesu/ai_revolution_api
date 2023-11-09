from djoser.serializers import UserSerializer
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    gpt3_tokens = serializers.IntegerField(read_only='gpt3_tokens')
    gpt4_tokens = serializers.IntegerField(read_only='gpt4_tokens')

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + \
            ('first_name', 'last_name', 'gpt3_tokens', 'gpt4_tokens')

    def to_representation(self, instance):
        print("CustomUserSerializer applied")
        return super().to_representation(instance)
