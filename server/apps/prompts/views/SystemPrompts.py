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
        operation_summary='Список системных ролей.',
        operation_description='''
        ### Получает все системные роли. Загружаются из файла/вносятся через административную панель.
        
        Значения:
        - `id`: id роли, \n
        - `title` - Название роли
        - `description` - Краткое описание роли
        - `prompt` - Текст системного промта для запроса к chatGPT
        '''
    )
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
