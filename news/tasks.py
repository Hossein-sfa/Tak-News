from bs4 import BeautifulSoup as bs
from selenium import webdriver
from celery import shared_task
from time import sleep
import requests

from .models import News, Tag


@shared_task()
def crawl_news():
    """
    Crawls news articles from a website and saves them to a database.
    This function uses a web driver to navigate through the website's news archive pages and extract information from each news article.
    The information includes the title, content, source URL, and tags of the news article.
    The function checks if each news article already exists in the database or not.
    If an article exists in database, the crawling process stops.
    Returns:
        None
    Raises:
        Exception: If an error occurs during the crawling process.
    """
    
    added_news = 0
    page_number = 1
    news_archive_url = 'https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber='
    
    # Loop through pages (up to 500)
    while page_number <= 500:
        try:
            driver = webdriver.Chrome()
            driver.get(news_archive_url + str(page_number))
            sleep(5)  # Wait for page to load and avoid throttling
            
            # Parse the page source
            beautiful_soup = bs(driver.page_source, 'html.parser')
            
            # Find all news article links
            news_links_tags = beautiful_soup.findAll('a', attrs={
                'class': 'link__CustomNextLink-sc-1r7l32j-0 eoKbWT BrowseArticleListItemDesktop__WrapperLink-zb6c6m-6 bzMtyO'})
            
            page_number += 1
            
            # Process each news article
            for link_tag in news_links_tags:
                link = link_tag['href']
                
                # Check if the news article already exists in the database
                if not News.objects.filter(source=link).exists():
                    # Fetch and parse the article page
                    soup = bs(requests.get(link).content, 'html.parser')
                    
                    # Extract title
                    header = soup.find('h1',
                                       attrs={'class': 'typography__StyledDynamicTypographyComponent-t787b7-0 fzMmhL'}) \
                             or soup.find('h1',
                                          attrs={
                                              'class': 'typography__StyledDynamicTypographyComponent-t787b7-0 jQMKGt'})
                    title = header.get_text()
                    
                    # Extract tags
                    tags_elements = soup.find('div', attrs={'class': 'flex__Flex-le1v16-0 kDyGrB'})
                    a_tags = tags_elements.findAll('a')
                    
                    # Extract content
                    paragraphs_tags = soup.findAll('p', attrs={
                        'class': 'typography__StyledDynamicTypographyComponent-t787b7-0 fZZfUi ParagraphElement__ParagraphBase-sc-1soo3i3-0 gOVZGU'})
                    paragraphs = [p.get_text() for p in paragraphs_tags]
                    content = '\n'.join(paragraphs)
                    
                    # Create new News object
                    crawled_news = News.objects.create(title=title, content=content, source=link)
                    
                    # Create or get Tag objects and add them to the News object
                    tags_objects = [Tag.objects.get_or_create(name=tag.get_text())[0] for tag in a_tags]
                    crawled_news.tags.add(*tags_objects)
                    crawled_news.save()
                    
                    added_news += 1
                else:
                    # If the article already exists, stop crawling because rest are already crawled
                    print('crawled news: ' + str(added_news))
                    driver.quit()
                    return
        except Exception as e:
            print(e)
    
    # Close the WebDriver
    driver.quit()
