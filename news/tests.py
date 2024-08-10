from django.urls import reverse
from django.test import Client, TestCase
from .models import News, Tag


class NewsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('news-list')
        
        # Create sample news items
        self.tech_news = News.objects.create(title="Tech News", content="New gadget released", source="www.Google.com")
        self.sports_news = News.objects.create(title="Sports Update", content="Team wins championship", source="www.Google.com")
        self.political_news = News.objects.create(title="Political News", content="New policy announced", source="www.Google.com")
        
        # Create sample tags
        self.tech_tag = Tag.objects.create(name="Technology")
        self.health_tag = Tag.objects.create(name="Health")
        self.sports_tag = Tag.objects.create(name="Sports")
        self.politics_tag = Tag.objects.create(name="Politics")
        
        # Add tags to news items
        self.tech_news.tags.add(self.tech_tag)
        self.sports_news.tags.add(self.sports_tag, self.health_tag)
        self.political_news.tags.add(self.politics_tag)

    def test_news_list_no_filter(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_news_list_filter_single_tag(self):
        response = self.client.get(self.url, {'filter': 'Technology'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Tech News")

    def test_news_list_filter_multiple_tags(self):
        response = self.client.get(self.url, {'filter': 'Health-Sports'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Sports Update")

    def test_news_list_filter_no_results(self):
        response = self.client.get(self.url, {'filter': 'Entertainment'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
