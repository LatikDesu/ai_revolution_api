from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from prompts.models import SystemPrompt
from prompts.serializers import SystemPromptSerializer


class SystemPromptList(generics.ListAPIView):

    queryset = SystemPrompt.objects.all()
    serializer_class = SystemPromptSerializer

    @swagger_auto_schema(
        tags=['System prompts'],
        responses={200: SystemPromptSerializer(many=True), },
        operation_summary='Список системных промптов.',
        operation_description='''
        ### Получает все системные промпты. Загружаются из файла/вносятся через административную панель.
        
        Значения:
        - `id`: id записи, \n
        - `title` - Название промпта
        - `description` - Краткое описание промпта
        - `prompt` - Текст системного промта для запроса к chatGPT
        '''
    )
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
