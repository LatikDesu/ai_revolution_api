
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from conversations.models import Conversation
from conversations.serializers import (
    ConversationSerializer,
    ConversationListSerializer
)

User = get_user_model()


# List and create conversations
class ChatListCreate(generics.ListCreateAPIView):
    """
    List and create chats.
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
        operation_id='chat_list',
        responses={200: ConversationListSerializer(many=True),
                   400: 'BAD REQUEST',
                   403: 'FORBIDDEN',
                   404: 'NOT FOUND'},
        operation_summary='Список всех чатов аутентифицированного пользователя.',
    )
    def get(self, request, *args, **kwargs):
        """
        ### Получает список всех чатов, созданных аутентифицированным пользователем, расположенные по дате обновления, от новых к старым.

        Значения:
        - `id`: id чата в формате uuid, \n
        - `title`: Заголовок чата,
        - `createdAt`: Дата создания,
        - `updatedAt`: Дата обновления
        """
        return self.list(request, *args, **kwargs)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ConversationListSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Conversations'],
        operation_id='chat_create',
        request_body=ConversationSerializer,
        responses={201: ConversationSerializer,
                   400: 'Bad Request',
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Создание нового чата аутентифицированного пользователя.',
    )
    def post(self, request, *args, **kwargs):
        '''
        ### Создает новый чат для аутентифицированного пользователя.

        Доступные параметры:
        - `title`: Заголовок чата (`default` = "Новый чат"), \n
        - `model`: Используемая модель (`default` = "gpt-3.5-turbo-0613"),
        - `prompt`: Системный промт (`default` = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown. Respond in the language of the request. The assistant is helpful, creative, clever, and very friendly. Ask your questions in Markdown format."),
        - `maxTokens`: Ограничение токенов в ответе (`default` = 500),
        - `temperature`: Температура ответа (`default` = 0,7),
        - `topP`: параметр nucleus sampling. Он определяет вероятность, с которой ChatGPT будет выбирать наиболее вероятные слова из своей модели при генерации текста. Чем выше значение top_p (максимум 1), тем более "предсказуемым" и менее разнообразным будет сгенерированный текст (`default` = 1),
        - `frequencyPenalty`: штраф за частоту. Этот параметр позволяет снизить вероятность слишком часто встречающихся в обучающей выборке фраз в ответах. Чем выше значение, тем менее вероятно повторение общих фраз из обучающей выборки (`default` = 0),
        - `presencePenalty`: штраф за наличие. Этот параметр позволяет снизить вероятность фрагментов текста, похожих на фрагменты в запросе, в ответах ChatGPT. Более высокое значение означает, что ChatGPT будет стараться избегать повторения частей исходного запроса в ответах (`default` = 0)
        '''
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
