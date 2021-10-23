import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
import re

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
    soup = bs(response.text, 'html.parser')
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
            salary_currency = None
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


def main():
    vacancy = 'Python'
    df = parser_vacancy(vacancy)
    pprint(df[:])


main()
