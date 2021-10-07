import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
import re
from pymongo import MongoClient

headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'}


def hh_parser(vacancy_str):
    params = {
        'text': vacancy_str,
        'search_field': 'name',
        'items_on_page': '100',
        'page': ''
    }
    base_url = 'https://hh.ru/search/vacancy'
    vacancy_data = []
    response = requests.get(base_url, params=params, headers=headers)
    soup =  bs(response.text, 'html.parser')
    page_block = soup.find('div', {'data-qa': 'pager-block'})
    if not page_block:
        last_page = '1'
    else:
        last_page_num = page_block.find_all('a', {'class': 'bloko-button', "data-qa": "pager-page"})[-1].getText()
        last_page = int(last_page_num)

    for page in range(0, last_page):
        params['page'] = page
        html = requests.get(base_url, params=params, headers=headers)
        parsed_html = bs(html.text, 'html.parser')
        vacancy_items = parsed_html.find('div', {'data-qa': 'vacancy-serp__results'}).find_all('div', {'class': 'vacancy-serp-item'})
        for item in vacancy_items:
            vacancy_data.append(hh_item_parser(item))
        return vacancy_data


def hh_item_parser(item):
    vacancy_list = {}

    vacancy_name = item.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).getText()
    vacancy_list['vacancy_name'] = vacancy_name

    salary = item.find('div', {'class': 'vacancy-serp-item__sidebar'})

    if not salary or salary == '':
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText() \
            .replace(u'\xa0', u'')

        salary = re.split(r'\s|-', salary)

        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1] + salary[2])
        elif salary[0] == 'от':
            salary_min = int(salary[1] + salary[2])
            salary_max = None
        elif salary[0] == '':
            salary_min = None
            salary_max = None
            salary_currency = ''
        else:
            salary_min = int(salary[0] + salary[1])
            salary_max = int(salary[3] + salary[4])
        salary_currency = salary[-1]

    vacancy_list['salary_min'] = salary_min
    vacancy_list['salary_max'] = salary_max
    vacancy_list['salary_currency'] = salary_currency

    vacancy_link = item.find('div', {'class': 'vacancy-serp-item__info'}).find('a')['href']
    vacancy_list['vacancy_link'] = vacancy_link
    vacancy_list['site'] = 'hh.ru'

    return vacancy_list


def parser_vacancy(vacancy):
    vacancy_date = []
    vacancy_date.extend(hh_parser(vacancy))

    df = pd.DataFrame(vacancy_date)

    return df

#1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию. Добавить в решение со сбором вакансий(продуктов) функцию,
#   которая будет добавлять только новые вакансии/продукты в вашу базу.

def mongo_db_processor():
    client = MongoClient('127.0.0.1', 27017)
    db = client['vacancies']
    hh = db.hh
    return db


#

def db_input_and_check(database, vacancy_date):
    for elt in vacancy_date:
        check_log = database.find({'link': vacancy_date["vacancy_link"]})
        if len(check_log)!= 0:
            pass
        else:
            database.insert({
                elt
            })
    return database

#2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты -
#   минимальнную и максимульную). Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска продуктов с
#   рейтингом не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна, а запрос проверяет оба поля)


def db_search_selector(database):
    sas = int(input('Введите искомый уровень з/п\n'))
    for doc in  database.find({{'salary.min_salary'}:{'$gte': sas}}):
        for elt in doc:
            print(elt)


def main():
    vacancy = 'Python'
    df = parser_vacancy(vacancy)
    pprint(df[:])
    df.to_csv(index=False)
    db_input_and_check(mongo_db_processor(), df)
    db_search_selector(database)


main()
