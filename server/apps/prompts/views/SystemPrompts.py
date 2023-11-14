from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from prompts.models import SystemPrompt
from prompts.serializers import SystemPromptSerializer


class SystemPromptList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = SystemPrompt.objects.all()
    serializer_class = SystemPromptSerializer

    @swagger_auto_schema(
        responses={200: SystemPromptSerializer(many=True)},
        operation_summary='Список системных ролей.',
        operation_description='Получает все системные роли.'
    )
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
