from django.contrib import admin

from .models import News, Tag


admin.site.register(Tag)
admin.site.register(News)
