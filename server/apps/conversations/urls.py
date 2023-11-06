from django.urls import path
from rest_framework.routers import DefaultRouter

from conversations.views.Conversations import (
    ConversationDelete,
    ConversationListCreate,
    MessageCreate,
    MessageList,
)


urlpatterns = [
    # List and create conversations
    path('', ConversationListCreate.as_view(),
         name='conversation-list-create'),

    # Retrieve, update, and delete a specific conversation
    # path('<int:pk>/', ConversationDetail.as_view(),
    #      name='conversation-detail'),

    # Delete a conversation
    path('<int:pk>/delete/',
         ConversationDelete.as_view(), name='conversation-delete'),

    # List messages in a conversation
    path('<int:conversation_id>/messages/',
         MessageList.as_view(), name='message-list'),

    # Create a message in a conversation
    path('<int:conversation_id>/messages/create/',
         MessageCreate.as_view(), name='message-create'),

]
