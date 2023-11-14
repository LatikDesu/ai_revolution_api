from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import AnonymousUser

from prompts.models import UserPrompt
from prompts.serializers import UserPromptSerializer


class UsersPromptsListCreate(generics.ListCreateAPIView):
    """
    List and create user prompts.
    """
    serializer_class = UserPromptSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserPromptSerializer(many=True)},
        operation_summary='Список всех ролей аутентифицированного пользователя.',
        operation_description='Получает все роли, созданные аутентифицированным пользователем.'
    )
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return UserPrompt.objects.none()
        user_prompts = UserPrompt.objects.filter(
            user=user).order_by('created_at')
        serializer = self.get_serializer(user_prompts, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserPromptSerializer,
        responses={201: UserPromptSerializer, },
        operation_summary='Создание новой роли аутентифицированного пользователя.',
        operation_description='''
        Создает новую роль для аутентифицированного пользователя.
        
        'title' - Название роли (default = "Custom role")
        'description' - Краткое описание роли (default = "Custom role") 
        'prompt' - Текст системного промта для запроса к chatGPT (default = null)
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
            return UserPrompt.objects.none()
        return UserPrompt.objects.filter(user=user)

    @swagger_auto_schema(
        responses={200: UserPromptSerializer,
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Получение информации о роли аутентифицированного пользователя.',
        operation_description='Получение информации о конкретной роли аутентифицированного пользователя.'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserPromptSerializer,
        responses={200: UserPromptSerializer,
                   400: 'Bad Request',
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Обновление информации о роли аутентифицированного пользователя.',
        operation_description='''
        Обновление информации о конкретной роли для аутентифицированного пользователя.
        
        'title' - Название роли (default = "Custom role")
        'description' - Краткое описание роли (default = "Custom role") 
        'prompt' - Текст системного промта для запроса к chatGPT (default = null)
        '''
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        auto_schema=None,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Удаление роли аутентифицированного пользователя.',
        operation_description='Удаление конкретной роли аутентифицированного пользователя.',
        responses={204: 'No Content',
                   403: 'Forbidden',
                   404: 'Not Found'},
    )
    def delete(self, request, *args, **kwargs):
        prompt = self.get_object()
        if prompt.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
