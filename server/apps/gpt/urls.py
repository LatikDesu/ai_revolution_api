from django.urls import path
from gpt.views import ConversationView

urlpatterns = [
    path('conversation/', ConversationView.as_view(), name='gpt-conversation' )
]