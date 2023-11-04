from djoser.serializers import UserSerializer
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    tokens = serializers.IntegerField(read_only='tokens')

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('tokens', )

    def to_representation(self, instance):
        print("CustomUserSerializer applied")
        return super().to_representation(instance)
