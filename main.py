import requests
from bs4 import BeautifulSoup
import csv
import os
import random

URL = 'https://respect-shoes.ru/catalog/fittin/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'accept': '*/*'}
FILE = 'shoes.csv'
HOST = 'https://respect-shoes.ru/'
numbers = random.sample(range(1, 37), k=5)


def get_html(url, params=None):
    result = requests.get(url, headers=HEADERS, params=params)
    return result


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="cards__item")
    charact_list = []
    for item in items:
        if int(item['data-prod-position']) in numbers:
            charact_list.append({
                'Название': item.find('span', class_="card__title").get_text(),
                'Цена': item.find('span', class_="card__price-num").get_text(),
                'Материал верха': item['data-prod-top-material'],
                'Материал низа': item['data-prod-lining-material'],
                'Сезон': item['data-prod-season'],
                'Номер': item['data-prod-position']
            })
    return charact_list


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([
            'Название',
            'Цена',
            'Материал верха',
            'Материал низа',
            'Сезон'
        ])
        for item in items:
            writer.writerow([
                item['Название'],
                item['Цена'],
                item['Материал верха'],
                item['Материал низа'],
                item['Сезон']
            ])


def parse():
    spisok = []
    for page in [1, 3, 8]:
        print(f'Парсинг страницы {page}')
        html = get_html(URL, params={'PAGEN_3': page})
        spisok.extend(get_content(html.text))
    save_file(spisok, FILE)
    print(spisok)
    os.startfile(FILE)


parse()