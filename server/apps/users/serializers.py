from djoser.serializers import UserSerializer
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + \
            ('first_name', 'last_name')

    def to_representation(self, instance):
        print("CustomUserSerializer applied")
        return super().to_representation(instance)
