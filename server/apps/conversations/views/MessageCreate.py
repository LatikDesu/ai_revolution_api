from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from conversations.models import Conversation
from conversations.serializers import MessageSerializer


class MessageCreate(APIView):
    """
    Save a message in current chat.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Conversation messages"],
        request_body=MessageSerializer,
        responses={
            201: MessageSerializer,
        },
        operation_id="chat_message_create",
        operation_summary="Cохранить сообщение в текущий чат.",
        manual_parameters=[
            openapi.Parameter(
                "conversation_id",
                openapi.IN_PATH,
                description="ID чата в котором работаем.",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        """
        ### Сохранить сообщение в текущий чат.

        Доступные параметры:
        - `content`: текст сообщения, \n
        - `role`: исполнитель сообщения (`user` или `assistant`)
        """

        conversation = get_object_or_404(
            Conversation, id=self.kwargs["conversation_id"], user=self.request.user
        )

        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(conversation=conversation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
