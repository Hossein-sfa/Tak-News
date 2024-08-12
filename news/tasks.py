from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
import requests

from .models import News, Tag


def crawl_news():
    added_news = 0
    page_number = 1
    news_archive_url = 'https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber='
    driver = webdriver.Chrome()
    while page_number <= 500:
        try:
            driver.get(news_archive_url + str(page_number))
            sleep(5)
            beautiful_soup = bs(driver.page_source, 'html.parser')
            news_links_tags = beautiful_soup.findAll('a', attrs={
                'class': 'link__CustomNextLink-sc-1r7l32j-0 eoKbWT BrowseArticleListItemDesktop__WrapperLink-zb6c6m-6 bzMtyO'})
            page_number += 1
            for link_tag in news_links_tags:
                link = link_tag['href']
                if not News.objects.filter(source=link).exists():
                    soup = bs(requests.get(link).content, 'html.parser')
                    header = soup.find('h1',
                                       attrs={'class': 'typography__StyledDynamicTypographyComponent-t787b7-0 fzMmhL'}) \
                             or soup.find('h1',
                                          attrs={
                                              'class': 'typography__StyledDynamicTypographyComponent-t787b7-0 jQMKGt'})
                    title = header.get_text()
                    tags_elements = soup.find('div', attrs={'class': 'flex__Flex-le1v16-0 kDyGrB'})
                    a_tags = tags_elements.findAll('a')
                    paragraphs_tags = soup.findAll('p', attrs={
                        'class': 'typography__StyledDynamicTypographyComponent-t787b7-0 fZZfUi ParagraphElement__ParagraphBase-sc-1soo3i3-0 gOVZGU'})
                    paragraphs = [p.get_text() for p in paragraphs_tags]
                    content = '\n'.join(paragraphs)
                    crawled_news = News.objects.create(title=title, content=content, source=link)
                    tags_objects = [Tag.objects.get_or_create(name=tag.get_text()) for tag in a_tags]
                    crawled_news.tags.add(*tags_objects)
                    crawled_news.save()
                    added_news += 1
                else:
                    print('crawled news: ' + str(added_news))
                    driver.quit()
                    return
        except Exception as e:
            print(e)
    print('crawled news: ' + str(added_news))
    driver.quit()
