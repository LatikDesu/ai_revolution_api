from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import AnonymousUser

from notekeeper.models import Note
from notekeeper.serializers import NoteListSerializer, NoteSerializer


class NoteList(generics.ListAPIView):
    """
    List user note.
    """
    serializer_class = NoteListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return Note.objects.filter(user=user).order_by('created_at')

    @swagger_auto_schema(
        responses={200: NoteListSerializer(many=True)},
        operation_summary='Список всех заметок аутентифицированного пользователя.',
        operation_description='Получает все заметки, созданные аутентифицированным пользователем.'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class NoteCreate(generics.CreateAPIView):
    """
    Create user note.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return Note.objects.filter(user=user)

    @swagger_auto_schema(
        request_body=NoteSerializer,
        responses={201: NoteSerializer, },
        operation_summary='Создание новой заметки аутентифицированного пользователя.',
        operation_description='''
        Создает заметку аутентифицированного пользователя.
        
        'note_title' - Заголовок заметки (default = "New Note")
        'note_content' - Содержание заметки (default = null) 
        '''
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a user note.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response([])
        return Note.objects.filter(user=user)

    @swagger_auto_schema(
        responses={200: NoteSerializer,
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Получение информации о заметке аутентифицированного пользователя.',
        operation_description='''
        Получение информации о конкретной заметке аутентифицированного пользователя.
        
        "id": id заметки в формате uuid,
        "user": id пользователя-владельца,
        "note_title": заголовок заметки,
        "note_content": содержание заметки в формате markdown,
        "slug": уникальное имя заметки, формируется автоматически из заголовка
        '''
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=NoteSerializer,
        responses={200: NoteSerializer,
                   400: 'Bad Request',
                   403: 'Forbidden',
                   404: 'Not Found'},
        operation_summary='Обновление данных в заметке аутентифицированного пользователя.',
        operation_description='''
        Обновление данных в конкретной заметке для аутентифицированного пользователя.
        
        "note_title": заголовок заметки,
        "note_content": содержание заметки в формате markdown,
        "slug": уникальное имя заметки, формируется автоматически из заголовка
        '''
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        auto_schema=None,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Удаление заметки аутентифицированного пользователя.',
        operation_description='Удаление конкретной заметки аутентифицированного пользователя.',
        responses={204: 'No Content',
                   403: 'Forbidden',
                   404: 'Not Found'},
    )
    def delete(self, request, *args, **kwargs):
        note = self.get_object()
        if note.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)


class CreateShareableLink(APIView):
    """
    Create a shareable link for a note.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Создание ссылки на заметку.',
        operation_description='Создание ссылки на конкретную заметку аутентифицированного пользователя с шифрованием данных',
        responses={201: 'shareable_link',
                   403: 'Forbidden',
                   404: 'Not Found'},
    )
    def post(self, request, note_id):
        try:
            note = get_object_or_404(Note, pk=note_id)
            shareable_link = note.get_absolute_url()
            return Response({'shareable_link': shareable_link}, status=status.HTTP_201_CREATED)
        except (Note.DoesNotExist, ValidationError):
            return Response({'detail': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)


class GetSharedNote(APIView):
    """
    Get the shared note from a shareable link.
    """
    @swagger_auto_schema(
        operation_summary='Расшифровка ссылки на заметку.',
        operation_description='Расшифровывает конкретную заметку аутентифицированного пользователя из ссылки',
        responses={200: NoteSerializer,
                   403: 'Forbidden',
                   404: 'Not Found'},
    )
    def get(self, request, shareable_id):
        try:
            pk = Note.signer.unsign(shareable_id)
            note = get_object_or_404(Note, pk=pk)
            serialized_note = {
                'note_title': note.note_title,
                'note_content': note.note_content,
                'slug': note.slug,
                'created_at': note.created_at,
                'updated_at': note.updated_at,
            }
            return Response(serialized_note, status=status.HTTP_200_OK)
        except Note.DoesNotExist:
            raise NotFound(detail='Note not found.')
        except:
            raise NotFound(detail='Invalid shareable link.')
