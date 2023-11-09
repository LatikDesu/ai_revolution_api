from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from conversations.models import Conversation, Folder
from conversations.serializers import FolderConversationSerializer, FolderSerializer


class FolderListView(generics.ListAPIView):

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user).order_by('created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for folder_data in data:
            folder_id = folder_data['id']
            conversations = Conversation.objects.filter(folder_id=folder_id)
            conversation_serializer = FolderConversationSerializer(
                conversations, many=True)
            folder_data['conversations'] = conversation_serializer.data

        return Response(data)


class FolderCreateView(generics.CreateAPIView):

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FolderDeleteView(generics.DestroyAPIView):

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        folder = self.get_object()

        if folder.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        folder.conversations.all().update(folder=None)

        folder.delete()

        return Response({"message": "folder deleted"}, status=status.HTTP_200_OK)


class FolderUpdateView(generics.UpdateAPIView):

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)
