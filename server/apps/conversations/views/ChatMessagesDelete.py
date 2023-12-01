from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from conversations.models import Message
from conversations.serializers import MessageSerializer

User = get_user_model()


class DeleteMessagesInChatView(generics.DestroyAPIView):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Conversations'],
        operation_id='delete_messages_in_chat',
        operation_summary='Очистка сообщений из указанного чата.',
        manual_parameters=[
            openapi.Parameter(
                'conversation_id',
                openapi.IN_PATH,
                description='ID чата, из которого нужно удалить сообщения.',
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: 'NO CONTENT',
                   403: 'FORBIDDEN',
                   404: 'NOT FOUND'},
    )
    def delete(self, request, *args, **kwargs):
        """
        ### Удаление всех сообщений из чата аутентифицированного пользователя.
        """
        conversation_id = self.kwargs['conversation_id']
        Message.objects.filter(conversation_id=conversation_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
