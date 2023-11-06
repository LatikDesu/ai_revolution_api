from django.urls import path
from rest_framework.routers import DefaultRouter

from conversations.views.Conversations import (
    ConversationDelete,
    ConversationListCreate,
    MessageCreate,
    MessageList,
    ConversationRetrieveUpdateView,
    DeleteMessagesInConversationView
)


urlpatterns = [
    # List and create conversations
    path('', ConversationListCreate.as_view(),
         name='conversation-list-create'),

    # Retrieve, update, and delete a specific conversation
    # path('<int:pk>/', ConversationDetail.as_view(),
    #      name='conversation-detail'),

    # Delete a conversation
    path('<int:conversation_id>/delete/',
         ConversationDelete.as_view(), name='conversation-delete'),

    # List messages in a conversation
    path('<int:conversation_id>/messages/',
         MessageList.as_view(), name='message-list'),

    # Create a message in a conversation
    path('<int:conversation_id>/messages/create/',
         MessageCreate.as_view(), name='message-create'),

    # Clear messages in a conversation
    path('<int:conversation_id>/clear/', DeleteMessagesInConversationView.as_view(),
         name='delete-messages-in-conversation'),

    # Create or update title
    path('<int:conversation_id>/title/',
         ConversationRetrieveUpdateView.as_view(), name='conversation-title'),

]
