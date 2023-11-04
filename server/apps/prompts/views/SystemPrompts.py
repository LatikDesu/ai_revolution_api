from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from prompts.models import SystemPrompt
from prompts.serializers import SystemPromptSerializer


class SystemPromptList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = SystemPrompt.objects.all()
    serializer_class = SystemPromptSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
