from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import AnonymousUser

from conversations.models import Conversation, Message
from conversations.serializers import (
    ConversationConfigSerializer,
    ConversationSerializer,
)
from conversations.tasks import generate_title_request

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
        return Conversation.objects.filter(user=user).order_by('created_at')

    @swagger_auto_schema(
        tags=['Conversations'],
        responses={200: ConversationSerializer(many=True)},
        operation_summary='Список всех чатов аутентифицированного пользователя.',
        operation_description="""
        ### Получает список всех чатов, созданных аутентифицированным пользователем.
        
        Значения:
        - `id`: id чата в формате uuid, \n
        - `title`: Заголовок чата,
        - `model`: Используемая модель,
        - `prompt`: Системный промт,
        - `tokenLimit`: Ограничение токенов в ответе,
        - `maxLength`: Ограничение размера чата в токенах,
        - `temperature`: Температура ответа,
        - `created_at`: Дата создания,
        - `folder`: Папка где хранится чат
        """
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Conversations'],
        request_body=ConversationSerializer,
        responses={201: ConversationSerializer, },
        operation_summary='Создание нового чата аутентифицированного пользователя.',
        operation_description='''
        ### Создает нооовый чат для аутентифицированного пользователя.
        
        Доступные параметры:
        - `title`: Заголовок чата (`default` = "Новый чат"), \n
        - `model`: Используемая модель (`default` = "gpt-3.5-turbo-0613"),
        - `prompt`: Системный промт (`default` = "You are ChatGPT, a large language model trained by OpenAI. Follow the - user's instructions carefully. Respond using markdown. Respond in the language of the request"),
        - `tokenLimit`: Ограничение токенов в ответе (`default` = 1000),
        - `maxLength`: Ограничение размера чата в токенах (`default` = 10000),
        - `temperature`: Температура ответа (`default` = 0,7),
        - `folder`: Папка где хранится чат (`default` = null)
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
        - `maxLength`: Ограничение размера чата в токенах,
        - `temperature`: Температура ответа,
        - `folder`: Папка где хранится чат
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
        return Response({"message": "conversation deleted"}, status=status.HTTP_200_OK)


class ConversationRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Retrieve View to update or get the title
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    lookup_url_kwarg = 'conversation_id'

    def retrieve(self, request, *args, **kwargs):
        conversation = self.get_object()

        messages = Message.objects.filter(
            conversation=conversation).order_by('-created_at')[:10][::-1]

        if messages:
            message_list = []
            for msg in messages:
                if msg.is_from_user:
                    message_list.append(
                        {"role": "user", "content": msg.content})
                else:
                    message_list.append(
                        {"role": "assistant", "content": msg.content})

            task = generate_title_request.apply_async(args=(message_list,))
            my_title = task.get()
            my_title = my_title[:64]
            conversation.title = my_title
            conversation.save()
            serializer = self.get_serializer(conversation)
            return Response(serializer.data)
        else:
            return Response({"message": "No messages in conversation."}, status=status.HTTP_204_NO_CONTENT)
