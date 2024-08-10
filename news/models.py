from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'News'
