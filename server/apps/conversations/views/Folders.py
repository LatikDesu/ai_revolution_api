from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from conversations.models import Conversation, Folder
from conversations.serializers import FolderConversationSerializer, FolderSerializer


class FolderListView(generics.ListAPIView):

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
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

        conversations_without_folders = Conversation.objects.filter(
            folder__isnull=True, user=self.request.user).order_by('created_at')

        default_folder = {
            'id': None,
            'title': None,
            'conversations': FolderConversationSerializer(conversations_without_folders, many=True).data
        }

        data.append(default_folder)

        return Response(data)

    @swagger_auto_schema(
        tags=['Conversation folders'],
        responses={200: FolderSerializer(many=True)},
        operation_summary='Список всех папок аутентифицированного пользователя.',
        operation_description="""
        ### Получает список всех папок и их содержимого, созданных аутентифицированным пользователем.
        
        Значения:
        - `id`: id папки в формате uuid, \n
        - `title`: Заголовок папки,
        - `conversations`: Список чатов, хранящихся в данной папке,
        """
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FolderCreateView(generics.CreateAPIView):

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return Folder.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        tags=['Conversation folders'],
        request_body=FolderSerializer,
        responses={201: FolderSerializer, },
        operation_summary='Создание новой папки аутентифицированного пользователя.',
        operation_description='''
        ### Создает новую папку для хранения чатов аутентифицированного пользователя.
        
        Доступные параметры:
        - `title`: Заголовок папки (`default` = "Новая папка"), \n
        '''
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FolderDeleteView(generics.DestroyAPIView):

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return Folder.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        tags=['Conversation folders'],
        operation_summary='Удаление папки аутентифицированного пользователя.',
        operation_description='### Удаление конкретной папки аутентифицированного пользователя. Значение `folder` вложенных чатов станет `null`.',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='ID папки, которую нужно удалить.',
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={204: 'No Content',
                   403: 'Forbidden',
                   404: 'Not Found'},
    )
    def delete(self, request, *args, **kwargs):
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
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return Folder.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        tags=['Conversation folders'],
        request_body=FolderSerializer,
        responses={200: FolderSerializer,
                   400: 'Bad Request',
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Обновление заголовка папки аутентифицированного пользователя.',
        operation_description='''
        ### Обновление заголовка конкретной папки для аутентифицированного пользователя.
        
        Доступные параметры:
        - `title`: заголовок папки, \n
        ''',
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='ID папки, заголовок которой нужно изменить.',
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        auto_schema=None,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
