import os
from celery import Celery
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miningPlatform.settings')

app = Celery('miningPlatform')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: [cfg.name for cfg in apps.get_app_configs()])
