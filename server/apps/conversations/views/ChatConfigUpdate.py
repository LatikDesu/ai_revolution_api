from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from conversations.models import Conversation
from conversations.serializers import ConversationConfigSerializer

User = get_user_model()


# Retrieve and update conversation
class ChatConfigUpdate(generics.UpdateAPIView):
    """
    Retrieve, update a config conversation.
    """

    serializer_class = ConversationConfigSerializer
    lookup_url_kwarg = "conversation_id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return Conversation.objects.filter(user=user)

    @swagger_auto_schema(
        tags=["Conversations"],
        operation_id="chat_config_update",
        request_body=ConversationConfigSerializer,
        responses={
            201: ConversationConfigSerializer,
            400: "BAD REQUEST",
            403: "FORBIDDEN",
            404: "NOT FOUND",
        },
        operation_summary="Обновление данных чата аутентифицированного пользователя.",
    )
    def patch(self, request, *args, **kwargs):
        """
        ### Обновление данных для конкретного чата аутентифицированного пользователя.

        Доступные параметры:
        - `title`: Заголовок чата, \n
        - `model`: Используемая модель,
        - `prompt`: Системный промт,
        - `maxTokens`: Ограничение токенов в ответе,
        - `temperature`: Температура ответа,
        - `topP`: topP,
        - `frequencyPenalty`: Штраф за частоту,
        - `presencePenalty`: Штраф за наличие.
        """

        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        auto_schema=None,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
