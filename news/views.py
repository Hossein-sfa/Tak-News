from rest_framework import generics
from django.http import HttpResponse

from .serializers import NewsSerializer
from .models import News
from .tasks import crawl_news


class NewsView(generics.ListCreateAPIView):
    """
    A view for listing news articles.

    This view inherits from ListCreateAPIView, providing GET (list) and POST (create) methods.
    It uses the News model and NewsSerializer for data representation.

    The get_queryset method is overridden to provide custom filtering based on query parameters.
    If a filter parameter is provided, it filters the queryset based on tags.
    If no filter is provided, it returns the first 100 news articles.

    Attributes:
        model: The News model used for this view.
        serializer_class: The NewsSerializer used for serializing data.
    """

    model = News
    serializer_class = NewsSerializer

    # Filtering with query parameters like filter=Tag1-Tag2-Tag3
    def get_queryset(self):
        filters = self.request.query_params.get('filter')
        queryset = News.objects.all()
        if filters is None:
            return queryset[:100]
        # Splitting multiple tags with '-'
        filtered_tags = filters.split('-')
        for tag in filtered_tags:
            if tag:
                queryset = queryset.filter(tags__name__contains=tag)
        return queryset.distinct()


class NewsDetailView(generics.RetrieveAPIView):
    """
    A view for getting a single news article.

    This view inherits from RetrieveAPIView, a GET method for retrieving
    a specific news article by its primary key.

    It uses the News model and NewsSerializer for data representation.

    Attributes:
        queryset: The queryset of all News objects.
        serializer_class: The NewsSerializer used for serializing data.
        lookup_field: The field used for looking up the news article (primary key).
    """

    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'pk'


def test(request):
    crawl_news()
    return HttpResponse(status=204)
