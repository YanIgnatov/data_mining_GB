#1' Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru,
# yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
#
#    название источника;
#    наименование новости;
#    ссылку на новость;
#    дата публикации.


# Я написал парсер для Ленты.

from pprint import pprint
from lxml import html
import requests

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        'Chrome/94.0.4606.61 Safari/537.36'}

response = requests.get("https://lenta.ru/")
dom = html.fromstring(response.text)

items = dom.xpath("//*[@id='root']/section[2]/div/div/div[1]/section[1]")

all_news = []
###
for item in items:
    news = {}
    source = "https://lenta.ru/"
    title = item.xpath(".//div[contains(@class,'item')]/a[@href]/text()")
    link = item.xpath(".//div[contains(@class,'item')]/a[@href]/@href")
    date = item.xpath(".//../a/time/@datetime")

    news['source'] = []
    news['title'] = title
    for elt in link:
        news['source'].append('Лента.ру')
        if elt[:5] == 'https':
            pass
        else:
            link[link.index(elt)] = source + elt
    news['link'] = link
    news['date'] = date
    all_news.append(news)

pprint(all_news)

#2. Cложить собранные новости в БД


from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_base = db['news_collection']

news_base.insert_many(all_news)
