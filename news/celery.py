import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

app = Celery('news')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
