#! /usr/bin/env python3
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adherence_core.settings')

app = Celery('adherence_web_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
