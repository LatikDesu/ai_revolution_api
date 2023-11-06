from django.urls import path

from .views import NoteList, NoteCreate, NoteDetail, CreateShareableLink, GetSharedNote


urlpatterns = [
    # List user note.
    path('list/', NoteList.as_view(), name='note-list'),

    # Create user note.
    path('create/', NoteCreate.as_view(), name='note-create'),

    # Retrieve, update, and delete a user note.
    path('<int:pk>/', NoteDetail.as_view(), name='note-detail'),

    path('share/create-link/<int:note_id>/',
         CreateShareableLink.as_view(), name='create-shareable-link'),
    path('share/shared-note/<str:shareable_id>/',
         GetSharedNote.as_view(), name='get-shared-note'),

]
