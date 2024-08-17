from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'
    def ready(self):
        # Initializes Celery
        import news.celery
