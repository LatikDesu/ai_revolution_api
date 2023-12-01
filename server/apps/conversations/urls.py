from django.urls import path

from conversations.views.Messages import (
    MessageRegenerate,
)

from conversations.views.ChatListCreate import ChatListCreate
from conversations.views.ChatConfigUpdate import ChatConfigUpdate
from conversations.views.ChatDelete import ChatDelete
from conversations.views.ChatMessagesDelete import DeleteMessagesInChatView

from conversations.views.MessagesList import MessagesList
from conversations.views.MessageCreate import MessageCreate
from conversations.views.MessageDelete import MessageDelete

from conversations.views.ChatCompletionStream import ChatCompletionStream


urlpatterns = [

    # Create and list chats
    path('', ChatListCreate.as_view(),
         name='chats-list-create'),

    # Retrieve, update conversation
    path('<uuid:conversation_id>/config/', ChatConfigUpdate.as_view(),
         name='chat-config-update'),

    # Delete a conversation
    path('<uuid:conversation_id>/delete/',
         ChatDelete.as_view(), name='chat-delete'),

    # Clear messages in a chat
    path('<uuid:conversation_id>/clear/', DeleteMessagesInChatView.as_view(),
         name='delete-messages-in-chat'),


    # List messages in a current chat
    path('<uuid:conversation_id>/messages/list/',
         MessagesList.as_view(), name='chat-messages-list'),

    # Create a message in a conversation
    path('<uuid:conversation_id>/messages/create/',
         MessageCreate.as_view(), name='message-create'),

    # Delete a message in a current chat
    path('<uuid:conversation_id>/<uuid:message_id>/delete/',
         MessageDelete.as_view(), name='message-delete'),

    # Request for GPT
    path('<uuid:conversation_id>/stream/', ChatCompletionStream.as_view(), name='chat-stream'),







    #     # Regenerate a message in a conversation
    #     path('<uuid:conversation_id>/<uuid:message_id>/regenerate/',
    #          MessageRegenerate.as_view(), name='message-regenerate'),





]
