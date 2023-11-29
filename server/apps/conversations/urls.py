from django.urls import path

from conversations.views.Conversations import (
    ConversationDelete,
    ConversationDetail,
    ConversationListCreate,
)
from conversations.views.Messages import (
    DeleteMessagesInConversationView,
    MessageCreate,
    MessageList,
)

urlpatterns = [
    # Retrieve, update conversation
    path('<uuid:conversation_id>/config/', ConversationDetail.as_view(),
         name='conversation-detail'),

    # List and create conversations
    path('', ConversationListCreate.as_view(),
         name='conversation-list-create'),

    # Delete a conversation
    path('<uuid:conversation_id>/delete/',
         ConversationDelete.as_view(), name='conversation-delete'),

    # List messages in a conversation
    path('<uuid:conversation_id>/messages/',
         MessageList.as_view(), name='message-list'),

    # Create a message in a conversation
    path('<uuid:conversation_id>/messages/create/',
         MessageCreate.as_view(), name='message-create'),

    # Clear messages in a conversation
    path('<uuid:conversation_id>/clear/', DeleteMessagesInConversationView.as_view(),
         name='delete-messages-in-conversation'),

]
