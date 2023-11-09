from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from conversations.models import Conversation, Message
from conversations.serializers import (
    ConversationConfigSerializer,
    ConversationSerializer,
)
from conversations.tasks import generate_title_request

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


# Retrieve and update conversation
class ConversationDetail(generics.UpdateAPIView):
    """
    Retrieve, update a config conversation.
    """
    serializer_class = ConversationConfigSerializer
    lookup_url_kwarg = 'conversation_id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)


# Delete a conversation
class ConversationDelete(APIView):
    """
    Delete a conversation.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, conversation_id):
        conversation = get_object_or_404(
            Conversation, id=conversation_id, user=request.user)
        conversation.delete()
        return Response({"message": "conversation deleted"}, status=status.HTTP_200_OK)


class ConversationRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Retrieve View to update or get the title
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    lookup_url_kwarg = 'conversation_id'

    def retrieve(self, request, *args, **kwargs):
        conversation = self.get_object()

        messages = Message.objects.filter(
            conversation=conversation).order_by('-created_at')[:10][::-1]

        if messages:
            message_list = []
            for msg in messages:
                if msg.is_from_user:
                    message_list.append(
                        {"role": "user", "content": msg.content})
                else:
                    message_list.append(
                        {"role": "assistant", "content": msg.content})

            task = generate_title_request.apply_async(args=(message_list,))
            my_title = task.get()
            my_title = my_title[:64]
            conversation.title = my_title
            conversation.save()
            serializer = self.get_serializer(conversation)
            return Response(serializer.data)
        else:
            return Response({"message": "No messages in conversation."}, status=status.HTTP_204_NO_CONTENT)
