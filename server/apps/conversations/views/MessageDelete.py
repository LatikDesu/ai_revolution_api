
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from conversations.models import Conversation, Message

User = get_user_model()


class MessageDelete(APIView):
    """
    Delete a message.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Conversation messages'],
        operation_id='chat_message_delete',
        operation_summary='Удаление сообщения из выбранного чата.',
        operation_description='### Удаление конкретного сообщения из чата аутентифицированного пользователя.',
        manual_parameters=[
            openapi.Parameter(
                'conversation_id',
                openapi.IN_PATH,
                description='ID чата, где нужно удалить.',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'message_id',
                openapi.IN_PATH,
                description='ID сообщения, которое нужно удалить.',
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={204: 'NO CONTENT',
                   403: 'FORBIDDEN',
                   404: 'NOT FOUND'},
    )
    def delete(self, request, conversation_id, message_id):
        conversation = get_object_or_404(
            Conversation, id=conversation_id, user=request.user)
        if conversation:
            message = get_object_or_404(
                Message,
                id=message_id,
            )
            message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
