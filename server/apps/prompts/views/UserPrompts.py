from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import AnonymousUser
from drf_yasg import openapi

from prompts.models import UserPrompt
from prompts.serializers import UserPromptSerializer


class UsersPromptsListCreate(generics.ListCreateAPIView):
    """
    List and create user prompts.
    """
    serializer_class = UserPromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return UserPrompt.objects.filter(user=user).order_by('created_at')

    @swagger_auto_schema(
        tags=['User prompts'],
        responses={200: UserPromptSerializer(many=True)},
        operation_summary='Список всех ролей аутентифицированного пользователя.',
        operation_description='''
        ### Получает все роли, созданные аутентифицированным пользователем.
        
        Значения:
        - `id`: id роли, \n
        - `title`: Название роли,
        - `description`: Краткое описание роли,
        - `prompt`: Текст системного промта для запроса к chatGPT 
        '''
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['User prompts'],
        request_body=UserPromptSerializer,
        responses={201: UserPromptSerializer, },
        operation_summary='Создание новой роли аутентифицированного пользователя.',
        operation_description='''
        ### Создает новую роль для аутентифицированного пользователя.
        
        Доступные параметры:
        - `title` - Название роли (`default` = "Custom role") \n
        - `description` - Краткое описание роли (`default` = "Custom role") 
        - `prompt` - Текст системного промта для запроса к chatGPT (`default` = null)
        '''
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UsersPromptsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a user prompt.
    """
    serializer_class = UserPromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return UserPrompt.objects.filter(user=user)

    @swagger_auto_schema(
        tags=['User prompts'],
        responses={200: UserPromptSerializer,
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Получение информации о роли аутентифицированного пользователя.',
        operation_description='''
        ### Получение информации о конкретной роли аутентифицированного пользователя.
        
        Значения:
        - `id`: id роли, \n
        - `title`: Название роли,
        - `description`: Краткое описание роли,
        - `prompt`: Текст системного промта для запроса к chatGPT 
        ''',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='ID роли, которую нужно получить.',
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['User prompts'],
        request_body=UserPromptSerializer,
        responses={200: UserPromptSerializer,
                   400: 'Bad Request',
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Обновление данных роли аутентифицированного пользователя.',
        operation_description='''
        ### Обновление данных в конкретной роли для аутентифицированного пользователя.
        
        Доступные параметры:
        - `title` - Название роли (`default` = "Custom role") \n
        - `description` - Краткое описание роли (`default` = "Custom role") 
        - `prompt` - Текст системного промта для запроса к chatGPT (`default` = null)
        ''',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='ID роли, которую нужно изменить.',
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        auto_schema=None,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['User prompts'],
        operation_summary='Удаление роли аутентифицированного пользователя.',
        operation_description='### Удаление конкретной роли аутентифицированного пользователя.',
        responses={204: 'No Content',
                   403: 'Forbidden',
                   404: 'Not Found'},
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='ID роли, которую нужно удалить.',
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def delete(self, request, *args, **kwargs):
        prompt = self.get_object()
        if prompt.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
