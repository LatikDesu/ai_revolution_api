from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from drf_yasg import openapi

from conversations.tasks import event_stream, send_gpt_request
from conversations.models import Conversation, Message


class ChatCompletionStream(APIView):
    """
    Send a request to OpenAI API.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['GPT API'],
        operation_id='gpt_chat_completion',
        operation_summary='Получение ответа от GPT API.',
        manual_parameters=[
            openapi.Parameter(
                'conversation_id',
                openapi.IN_PATH,
                description='ID чата для которого делаем запрос.',
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        ### ПОЛУЧЕНИЕ ОТВЕТА ОТ GPT API.
        Берет 5 последних сообщений из чата и отправляет запрос на получение ответа от GPT API.
        Предвартительно текст запроса необходимо сохранить как сообщение в текущий чат
        `POST /conversations/{conversation_id}/messages/create/` (`role` = 'user')
        Полученный ответ возвращается в виде потока.
        Далее, после манипуляций с ответом на фронтэнде, необходимо сохранить его как сообщение в текущий чат. (`role` = 'assistant')
        """

        conversation = get_object_or_404(
            Conversation, id=self.kwargs['conversation_id'], user=self.request.user)

        messages = Message.objects.filter(
            conversation=conversation).order_by('-createdAt')[:5][::-1]

        message_list = []
        for msg in messages:
            if msg.role == 'user':
                message_list.append({"role": "user", "content": msg.content})
            else:
                message_list.append(
                    {"role": "assistant", "content": msg.content})

        # Build config for GPT from Conversation fields
        conversation_fields = ['model', 'prompt',
                               'maxTokens', 'temperature', 'topP', 'frequencyPenalty', 'presencePenalty']
        config = {field: getattr(conversation, field)
                  for field in conversation_fields}

        stream = send_gpt_request(message_list, config)

        response = StreamingHttpResponse(
            event_stream(stream), content_type="text/event-stream")
        response['X-Accel-Buffering'] = 'no'
        response['Cache-Control'] = 'no-cache'

        return response
