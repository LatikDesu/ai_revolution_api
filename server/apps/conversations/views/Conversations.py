
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from conversations.models import Conversation
from conversations.serializers import (
    ConversationConfigSerializer,
    ConversationSerializer,
)

User = get_user_model()


# List and create conversations
class ConversationListCreate(generics.ListCreateAPIView):
    """
    List and create conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return Conversation.objects.filter(user=user).order_by('-updatedAt')

    @swagger_auto_schema(
        tags=['Conversations'],
        responses={200: ConversationSerializer(many=True),
                   400: 'Bad Request',
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Список всех чатов аутентифицированного пользователя.',
        operation_description="""
        ### Получает список всех чатов, созданных аутентифицированным пользователем.

        Значения:
        - `id`: id чата в формате uuid, \n
        - `title`: Заголовок чата,
        - `model`: Используемая модель,
        - `prompt`: Системный промт,
        - `tokenLimit`: Ограничение токенов в ответе,
        - `temperature`: Температура ответа,
        - `createdAt`: Дата создания,
        - `updatedAt`: Дата обновления
        """
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Conversations'],
        request_body=ConversationSerializer,
        responses={201: ConversationSerializer,
                   400: 'Bad Request',
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Создание нового чата аутентифицированного пользователя.',
        operation_description='''
        ### Создает новый чат для аутентифицированного пользователя.

        Доступные параметры:
        - `title`: Заголовок чата (`default` = "Новый чат"), \n
        - `model`: Используемая модель (`default` = "gpt-3.5-turbo-0613"),
        - `prompt`: Системный промт (`default` = "You are ChatGPT, a large language model trained by OpenAI. Follow the - user's instructions carefully. Respond using markdown. Respond in the language of the request"),
        - `tokenLimit`: Ограничение токенов в ответе (`default` = 1000),
        - `temperature`: Температура ответа (`default` = 0,7),
        '''
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Retrieve and update conversation
class ConversationDetail(generics.UpdateAPIView):
    """
    Retrieve, update a config conversation.
    """
    serializer_class = ConversationConfigSerializer
    lookup_url_kwarg = 'conversation_id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return Conversation.objects.filter(user=user)

    @swagger_auto_schema(
        tags=['Conversations'],
        request_body=ConversationConfigSerializer,
        responses={200: ConversationConfigSerializer,
                   400: 'Bad Request',
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Обновление данных чата аутентифицированного пользователя.',
        operation_description='''
        ### Обновление данных для конкретного чата аутентифицированного пользователя.

        Доступные параметры:
        - `title`: Заголовок чата, \n
        - `model`: Используемая модель,
        - `prompt`: Системный промт,
        - `tokenLimit`: Ограничение токенов в ответе,
        - `temperature`: Температура ответа,
        '''
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        auto_schema=None,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


# Delete a conversation
class ConversationDelete(APIView):
    """
    Delete a conversation.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Conversations'],
        operation_summary='Удаление чата аутентифицированного пользователя.',
        operation_description='### Удаление конкретного чата аутентифицированного пользователя.',
        manual_parameters=[
            openapi.Parameter(
                'conversation_id',
                openapi.IN_PATH,
                description='ID чата, который нужно удалить.',
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={204: 'No Content',
                   403: 'Forbidden',
                   404: 'Not Found'},
    )
    def delete(self, request, conversation_id):

        conversation = get_object_or_404(
            Conversation, id=conversation_id, user=request.user)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
