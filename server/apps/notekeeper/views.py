from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notekeeper.models import Note
from notekeeper.serializers import NoteListSerializer, NoteSerializer


class NoteList(generics.ListAPIView):
    """
    List user note.
    """
    serializer_class = NoteListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('created_at')


class NoteCreate(generics.CreateAPIView):
    """
    Create user note.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a user note.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

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
