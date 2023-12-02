from django.contrib import admin

from .models import SystemPrompt


class SystemPromptsAdmin(admin.ModelAdmin):
    model = SystemPrompt

    list_display = (
        "title",
        "description",
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


admin.site.register(SystemPrompt, SystemPromptsAdmin)
