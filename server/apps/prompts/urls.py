from django.urls import path

from .views.SystemPrompts import SystemPromptList

urlpatterns = [
    path("systemprompts/", SystemPromptList.as_view(), name="systemprompt-list"),
]
