from django.urls import path

from .views.SystemPrompts import SystemPromptList
from .views.UserPrompts import UsersPromptsListCreate, UsersPromptsDetail


urlpatterns = [
    path('systemprompts/', SystemPromptList.as_view(), name='systemprompt-list'),

    # List and create user prompts.
    path('userprompts/', UsersPromptsListCreate.as_view(),
         name='usersprompts-list-create'),

    # Retrieve, update, and delete a user prompt.
    path('userprompts/<int:pk>/', UsersPromptsDetail.as_view(),
         name='usersprompts-detail'),

]
