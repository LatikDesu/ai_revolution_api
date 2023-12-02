from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from conversations.models import Conversation

User = get_user_model()


# Delete a conversation
class ChatDelete(APIView):
    """
    Delete a conversation.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Conversations"],
        operation_id="delete_chat",
        operation_summary="Удаление чата аутентифицированного пользователя.",
        manual_parameters=[
            openapi.Parameter(
                "conversation_id",
                openapi.IN_PATH,
                description="ID чата, который нужно удалить.",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            204: "NO CONTENT",
            400: "BAD REQUEST",
            403: "FORBIDDEN",
            404: "NOT FOUND",
        },
    )
    def delete(self, request, conversation_id):
        """
        ### Удаление конкретного чата аутентифицированного пользователя.
        """
        conversation = get_object_or_404(
            Conversation, id=conversation_id, user=request.user
        )
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
