from celery import Celery


app = Celery()

# Load celery configuration from django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load and register tasks from tasks.py
app.autodiscover_tasks()
