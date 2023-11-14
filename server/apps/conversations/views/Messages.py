from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from conversations.models import Conversation, Message
from conversations.serializers import (
    MessageSerializer,
)
from conversations.tasks import send_gpt_request

User = get_user_model()


class MessageList(generics.ListAPIView):
    """
    List messages in a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation = get_object_or_404(
            Conversation, id=self.kwargs['conversation_id'], user=self.request.user)
        return Message.objects.filter(conversation=conversation).select_related('conversation')

    @swagger_auto_schema(
        tags=['Conversation messages'],
        responses={200: MessageSerializer(many=True)},
        operation_summary='Список сообщений в беседе.',
        operation_description="""
        ### Получает список всех сообщений из беседы аутентифицированного пользователя.
        
        Значения:
        - `id`: id сообщения в формате uuid, \n
        - `conversation`: id чата в формате uuid,
        - `content`: текст запроса / ответа,
        - `is_from_user`: флаг, определяющий, является ли это сообщение от пользователя,
        - `in_reply_to`: id сообщения, в ответ на которое было данное сообщение,
        - `created_at`: время создания сообщения в формате ISO 8601,
        """,
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
        return self.list(request, *args, **kwargs)


class MessageCreate(generics.CreateAPIView):
    """
    Create a message in a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        conversation = get_object_or_404(
            Conversation, id=self.kwargs['conversation_id'], user=self.request.user)
        serializer.save(conversation=conversation, is_from_user=True)

        # Retrieve the last 5 messages from the conversation
        messages = Message.objects.filter(
            conversation=conversation).order_by('-created_at')[:5][::-1]

        # Build the list of dictionaries containing the message data
        message_list = []
        for msg in messages:
            if msg.is_from_user:
                message_list.append({"role": "user", "content": msg.content})
            else:
                message_list.append(
                    {"role": "assistant", "content": msg.content})

        # Build config for GPT-3 from Conversation fields
        conversation_fields = ['model', 'prompt',
                               'tokenLimit', 'maxLength', 'temperature']
        config = {field: getattr(conversation, field)
                  for field in conversation_fields}

        # Call the Celery task to get a response from GPT-3
        # task = send_gpt_request.apply_async(
        #     args=(message_list, config))
        # response = task.get()

        response = send_gpt_request(message_list, config)

        return [response, conversation.id, messages[0].id]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_list = self.perform_create(serializer)
        assistant_response = response_list[0]
        conversation_id = response_list[1]
        last_user_message_id = response_list[2]

        try:
            # Store GPT response as a message
            message = Message(
                conversation_id=conversation_id,
                content=assistant_response,
                is_from_user=False,
                in_reply_to_id=last_user_message_id
            )
            message.save()

        except ObjectDoesNotExist:
            error = f"Conversation with id {conversation_id} does not exist"
            Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_mgs = str(e)
            error = f"Failed to save GPT-3 response as a message: {error_mgs}"
            Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response({"response": assistant_response}, status=status.HTTP_200_OK, headers=headers)

    @swagger_auto_schema(
        tags=['Conversation messages'],
        request_body=MessageSerializer,
        responses={201: MessageSerializer, },
        operation_summary='Отправить запрос к ChatGPT.',
        operation_description='''
        ### Создает сообщение от имени пользователя к ChatGPT.
        
        Доступные параметры:
        - `content`: текст запроса, \n
        ''',
        manual_parameters=[
            openapi.Parameter(
                'conversation_id',
                openapi.IN_PATH,
                description='ID чата в котором работаем.',
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DeleteMessagesInConversationView(generics.DestroyAPIView):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Conversations'],
        operation_summary='Очистка сообщений из чата.',
        operation_description='### Удаление всех сообщений из чата аутентифицированного пользователя.',
        manual_parameters=[
            openapi.Parameter(
                'conversation_id',
                openapi.IN_PATH,
                description='ID чата, из которого нужно удалить сообщения.',
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: 'all messages deleted',
                   403: 'Forbidden',
                   404: 'Not Found'},
    )
    def delete(self, request, *args, **kwargs):
        conversation_id = self.kwargs['conversation_id']
        Message.objects.filter(conversation_id=conversation_id).delete()
        return Response({"message": "all messages deleted"}, status=status.HTTP_200_OK)
