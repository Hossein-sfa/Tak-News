from rest_framework import generics
from django.http import HttpResponse

from .serializers import NewsSerializer
from .models import News
from .tasks import crawl_news

class NewsView(generics.ListCreateAPIView):
    model = News
    serializer_class = NewsSerializer

    # Filtering with query parameters like filter=Tag1-Tag2-Tag3
    def get_queryset(self):
        filters = self.request.query_params.get('filter')
        queryset = News.objects.all()
        if filters is None:
            return queryset
        # Splitting multiple tags with '-'
        filtered_tags = filters.split('-')
        for tag in filtered_tags:
            if tag:
                queryset = queryset.filter(tags__name__contains=tag).distinct()
        return queryset


class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'pk'


def test(request):
    crawl_news()
    return HttpResponse(status=204)