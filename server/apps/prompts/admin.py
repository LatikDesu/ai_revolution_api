from django.contrib import admin

from .models import SystemPrompt, UserPrompt


class SystemPromptsAdmin(admin.ModelAdmin):
    model = SystemPrompt

    list_display = (
        'title',
        'description',
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "prompt",
                )
            },
        ),
    )
    search_fields = ("title",)
    ordering = ("id",)


class UserPromptsAdmin(admin.ModelAdmin):
    model = UserPrompt

    list_display = (
        'title',
        'description',
        'user'
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "prompt",
                    "user",
                )
            },
        ),
    )
    search_fields = ("title",)
    ordering = ("id",)


admin.site.register(SystemPrompt, SystemPromptsAdmin)
admin.site.register(UserPrompt, UserPromptsAdmin)
