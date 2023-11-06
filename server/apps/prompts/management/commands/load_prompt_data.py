import json
from pathlib import Path

from django.core.management.base import BaseCommand

from prompts.models import SystemPrompt

current_dir = Path(__file__).resolve().parent
system_prompts_data_file = current_dir / 'system_prompts_data.json'


class Command(BaseCommand):
    help = 'Load common data from JSON file'

    def handle(self, *args, **options):

        with open(system_prompts_data_file, 'r') as file:
            data = json.load(file)

        for item in data:
            prompt, created = SystemPrompt.objects.get_or_create(
                title=item['title'],
                defaults={'description': item['description'],
                          'prompt': item['prompt']}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created System Prompt: {prompt.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'System Prompt already exists: {prompt.title}'))
