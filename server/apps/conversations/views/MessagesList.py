from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from conversations.models import Conversation, Message
from conversations.serializers import ConversationSerializer

User = get_user_model()


class MessagesList(RetrieveAPIView):
    """
    List messages in a current chat.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Conversation messages'],
        operation_id='chat_messages_list',
        responses={200: ConversationSerializer},
        operation_summary='Список сообщений в выбраном чате.',

        manual_parameters=[
            openapi.Parameter(
                'conversation_id',
                openapi.IN_PATH,
                description='ID чата из которого получаем сообщения.',
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        ### Получает список всех сообщений из беседы аутентифицированного пользователя. Выводит данные о настройках конкретного чата и список сообщений в порядке даты создания от старых к новым.

        Структура ответа:
        - `id`: id чата в формате uuid, \n
        - `title`: Заголовок чата, \n
        - `model`: Используемая модель,
        - `prompt`: Системный промт,
        - `maxTokens`: Ограничение токенов в ответе,
        - `temperature`: Температура ответа,    
        - `topP`: topP,
        - `frequencyPenalty`: Штраф за частоту,
        - `presencePenalty`: Штраф за наличие.
        - `createdAt`: Дата создания,
        - `updatedAt`: Дата обновления
        - `messages`: [список сообщений]

        Значения полей для messages:
        - `id`: id сообщения в формате uuid, \n
        - `conversation`: id чата в формате uuid,
        - `content`: текст запроса / ответа,
        - `role`: источник сообщения (пользователь или бот),
        - `createdAt`: время создания сообщения в формате ISO 8601
        """

        chat = get_object_or_404(
            Conversation, id=self.kwargs['conversation_id'], user=self.request.user)
        messages = Message.objects.filter(
            conversation=chat).order_by('createdAt')

        serializer = self.get_serializer({'id': chat.id, 'title': chat.title, 'model': chat.model, 'prompt': chat.prompt, 'maxTokens': chat.maxTokens,
                                         'temperature': chat.temperature,
                                          'topP': chat.topP, 'frequencyPenalty': chat.frequencyPenalty, 'presencePenalty': chat.presencePenalty, 'createdAt': chat.createdAt, 'updatedAt': chat.updatedAt, 'messages': messages})

        return Response(serializer.data, status=status.HTTP_200_OK)
