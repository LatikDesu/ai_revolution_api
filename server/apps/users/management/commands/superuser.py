from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth import get_user_model
from os import getenv, path
import dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = BASE_DIR / '.env'

if path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

User = get_user_model()

DJANGO_SUPERUSER_PASSWORD = getenv('DJANGO_SUPERUSER_PASSWORD')
DJANGO_SUPERUSER_EMAIL = getenv('DJANGO_SUPERUSER_EMAIL')


class Command(BaseCommand):
    help = 'Create superuser'

    def handle(self, *args, **options):
        try:
            user = User(
                email=DJANGO_SUPERUSER_EMAIL,
            )
            user.set_password(DJANGO_SUPERUSER_PASSWORD)
            user.is_superuser = True
            user.is_staff = True
            user.is_admin = True
            user.save()
            self.stdout.write(self.style.SUCCESS(
                'Superuser created successfully'))
        except Exception as e:
            raise CommandError(e)
