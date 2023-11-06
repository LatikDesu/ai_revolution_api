from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from prompts.models import UserPrompt
from prompts.serializers import UserPromptSerializer


class UsersPromptsListCreate(generics.ListCreateAPIView):
    """
    List and create user prompts.
    """
    serializer_class = UserPromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPrompt.objects.filter(user=self.request.user).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UsersPromptsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a user prompt.
    """
    serializer_class = UserPromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserPrompt.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        prompt = self.get_object()
        if prompt.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
