from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from conversations.models import Conversation, Message
from conversations.serializers import ConversationSerializer, MessageSerializer
from conversations.tasks import send_gpt_request, event_stream

User = get_user_model()


class MessageList(RetrieveAPIView):
    """
    List messages in a conversation.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Conversation messages'],
        responses={200: ConversationSerializer},
        operation_summary='Список сообщений в беседе.',
        operation_description="""
        ### Получает список всех сообщений из беседы аутентифицированного пользователя. Выводит данные о настройках конкретного чата и список сообщений в порядке даты создания от старых к новым.
        
        Структура ответа:
        - `id`: id чата в формате uuid, \n
        - `title`: Заголовок чата,
        - `model`: Используемая модель,
        - `prompt`: Системный промт,
        - `tokenLimit`: Ограничение токенов в ответе,
        - `temperature`: Температура ответа,
        - `createdAt`: Дата создания,
        - `updatedAt`: Дата обновления
        - `messages`: [список сообщений]

        Значения полей для messages:
        - `id`: id сообщения в формате uuid, \n
        - `conversation`: id чата в формате uuid,
        - `content`: текст запроса / ответа,
        - `isFromUser`: флаг, определяющий, является ли это сообщение от пользователя,
        - `inReplyTo`: id сообщения, в ответ на которое было данное сообщение,
        - `createdAt`: время создания сообщения в формате ISO 8601,
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
        chat = get_object_or_404(
            Conversation, id=self.kwargs['conversation_id'], user=self.request.user)
        messages = Message.objects.filter(
            conversation=chat).order_by('createdAt')
        serializer = self.get_serializer({'id': chat.id, 'title': chat.title, 'model': chat.model, 'prompt': chat.prompt, 'tokenLimit': chat.tokenLimit,
                                         'temperature': chat.temperature, 'createdAt': chat.createdAt, 'updatedAt': chat.updatedAt, 'messages': messages})

        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageCreate(generics.CreateAPIView):
    """
    Create a message in a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, request, serializer, stream):
        conversation = get_object_or_404(
            Conversation, id=self.kwargs['conversation_id'], user=self.request.user)

        serializer.save(conversation=conversation, isFromUser=True)

        # Retrieve the last 5 messages from the conversation
        messages = Message.objects.filter(
            conversation=conversation).order_by('-createdAt')[:5][::-1]

        # Build the list of dictionaries containing the message data
        message_list = []
        for msg in messages:
            if msg.isFromUser:
                message_list.append({"role": "user", "content": msg.content})
            else:
                message_list.append(
                    {"role": "assistant", "content": msg.content})

        # Build config for GPT from Conversation fields
        conversation_fields = ['model', 'prompt',
                               'tokenLimit', 'temperature']
        config = {field: getattr(conversation, field)
                  for field in conversation_fields}

        response = send_gpt_request(message_list, config, stream)

        return [response, conversation.id, messages[-1].id]

    def create(self, request, *args, **kwargs):
        # Получаем данные из тела запроса
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stream = request.data.get('stream', True)

        # Отправляем запрос в GPT
        response_list = self.perform_create(
            request=request, serializer=serializer, stream=stream)

        # Разбираем ответ
        assistant_response = response_list[0]
        conversation_id = response_list[1]
        last_user_message_id = response_list[2]

        if stream:
            assistant_response_content = ""
            for part in assistant_response:
                assistant_response_content += part

        else:
            assistant_response_content = assistant_response

        try:
            # Store GPT response as a message
            message = Message(
                conversation_id=conversation_id,
                content=assistant_response_content,
                isFromUser=False,
                inReplyTo_id=last_user_message_id
            )
            message.save()

        except ObjectDoesNotExist:
            error = f"Conversation with id {conversation_id} does not exist"
            Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_mgs = str(e)
            error = f"Failed to save GPT-3 response as a message: {error_mgs}"
            Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        # Return the response
        if not stream:
            headers = self.get_success_headers(serializer.data)
            return Response({"response": assistant_response_content}, status=status.HTTP_200_OK, headers=headers)

        response = StreamingHttpResponse(
            event_stream(assistant_response), content_type="text/event-stream")
        response['X-Accel-Buffering'] = 'no'
        response['Cache-Control'] = 'no-cache'
        return response

    @swagger_auto_schema(
        tags=['Conversation messages'],
        request_body=MessageSerializer,
        responses={201: MessageSerializer, },
        operation_summary='Отправить запрос к ChatGPT.',
        operation_description='''
        ### Создает сообщение от имени пользователя к ChatGPT.

        Доступные параметры:
        - `content`: текст запроса, \n
        - `stream`: флаг, определяющий нужно ли возвращать ответ потоком (`default` = True)
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




class MessageRegenerate(APIView):
    """
    Regenerate a message.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Conversation messages'],
        operation_summary='Перегенерация сообщения в чате.',
        operation_description='### Перегенерация конкретного сообщения в чате аутентифицированного пользователя.',
        manual_parameters=[
            openapi.Parameter(
                'conversation_id',
                openapi.IN_PATH,
                description='ID чата, где нужно перегенерировать.',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'message_id',
                openapi.IN_PATH,
                description='ID сообщения, которое нужно перегенерировать.',
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: MessageSerializer,
                   403: 'Forbidden',
                   404: 'Not Found'},)
    def patch(self, request, conversation_id, message_id):
        conversation = get_object_or_404(
            Conversation, id=conversation_id, user=request.user)
        if conversation:
            message = get_object_or_404(
                Message,
                id=message_id,
            )

            new_content = regenerate(conversation, message)

            message.content = new_content
            message.save()

        return Response({"response": message.content}, status=status.HTTP_200_OK)


def regenerate(conversation, message):
    messages = Message.objects.filter(
        conversation=message.conversation).order_by('-createdAt')[:5][::-1]

    message_list = []
    for msg in messages:
        if msg.isFromUser:
            message_list.append({"role": "user", "content": msg.content})
        else:
            message_list.append(
                {"role": "assistant", "content": msg.content})

    conversation_fields = ['model', 'prompt',
                           'tokenLimit', 'temperature']
    config = {field: getattr(conversation, field)
              for field in conversation_fields}

    response = send_gpt_request(message_list[:-1], config, stream=False)

    return response
