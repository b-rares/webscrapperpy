import requests
from bs4 import BeautifulSoup
import string
import os

current_dir = os.getcwd()
page_number = 0
type_of_article_ = ''

def get_user_input():
    global page_number, type_of_article_
    number_of_pages = int(input())
    type_of_article = input()
    type_of_article_ = type_of_article
    for i in range(1,number_of_pages + 1):
        page_number = i
        response = get_response(i)
        get_bs(response, type_of_article)

def remove_punctuation(e):
    if e[len(e) - 1] in string.punctuation:
        return e[:-1]
    return e

def get_response(page_number):
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='
    url += str(page_number)
    r = requests.get(url)
    return r

def get_bs(response, type_of_article):
    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.find_all('span', string=type_of_article)
    news_articles = []
    for e in news:
        news_articles.append(e.parent.parent.parent)
    titles = []
    news_articles_link = []
    website = 'https://www.nature.com'
    news_content = []
    for article in news_articles:
        titles.append(article.a.text.strip())
        news_articles_link.append(article.a['href'])
    for link in news_articles_link:
        news_response = requests.get(website + link)
        soup = BeautifulSoup(news_response.content, 'html.parser')
        content = soup.find('div', attrs={'class': 'c-article-body u-clearfix'}).text
        news_content.append(content)
    write_files(titles, news_content)


def write_files(titles, articles):
    global current_dir,type_of_article_
    os.mkdir(f'Page_{page_number}')
    os.chdir(f'Page_{page_number}')
    for i in range(len(titles)):
        if titles[i][len(titles[i]) - 1] in string.punctuation:
            titles[i] = titles[i][:-1] + '.txt'
        else:
            titles[i] = titles[i] + '.txt'
    for index, value in enumerate(titles):
        value = value.translate(value.maketrans(' ', '_'))
        file = open(value, 'wb')
        file.write(bytes(articles[index], 'utf-8'))
        file.close()
    print(titles)
    os.chdir(current_dir)
get_user_input()
