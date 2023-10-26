from django.urls import path
from conversations.views.ConversationFlow import ConversationFlowView
from conversations.views.Conversation import ConversationViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('gpt_request/', ConversationFlowView.as_view(), name='conversation flow')
]

urlpatterns += router.urls
