from __future__ import absolute_import
import os
from celery import Celery
from django.apps import apps
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
app = Celery('src')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['apps'])


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
