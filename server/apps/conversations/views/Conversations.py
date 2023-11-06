from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from conversations.models import Conversation, Message
from conversations.serializers import (
    ConversationSerializer,
    MessageSerializer,
)
from conversations.tasks import send_gpt_request_task

User = get_user_model()


# List and create conversations
class ConversationListCreate(generics.ListCreateAPIView):
    """
    List and create conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Retrieve, update, and delete a specific conversation
class ConversationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a specific conversation.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        conversation = self.get_object()
        if conversation.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)


# Delete a conversation
class ConversationDelete(APIView):
    """
    Delete a conversation.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        conversation = get_object_or_404(
            Conversation, id=pk, user=request.user)
        conversation.delete()
        return Response({"message": "conversation deleted"}, status=status.HTTP_200_OK)


# List messages in a conversation
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


# Create a message in a conversation
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

        # Retrieve the last 10 messages from the conversation
        messages = Message.objects.filter(
            conversation=conversation).order_by('-created_at')[:10][::-1]

        # Build the list of dictionaries containing the message data
        message_list = []
        for msg in messages:
            if msg.is_from_user:
                message_list.append({"role": "user", "content": msg.content})
            else:
                message_list.append(
                    {"role": "assistant", "content": msg.content})

        system_prompt = "You are sonic you can do anything you want."
        # response = send_gpt_request(message_list, system_prompt)

        # Call the Celery task to get a response from GPT-3
        task = send_gpt_request_task.apply_async(
            args=(message_list, system_prompt))
        response = task.get()
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
