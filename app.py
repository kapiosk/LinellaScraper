#!venv/bin python3
# -*- coding: utf-8 -*-

import csv
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

current_datetime = datetime.datetime.utcnow()

baseUrl = 'https://linella.md'
html = urlopen(f'{baseUrl}/en').read()
soup = BeautifulSoup(html, features = 'html.parser')
generalCategories = soup.find_all('ul', class_ = 'level2')

header = ['category', 'page', 'name', 'price', 'normal_price', 'scan_time']

with open('items.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for gc in generalCategories:
        categories = gc.find_all('a', href = True)
        for category in categories:
            hasMorePages = True
            page = 1
            while hasMorePages:
                href = category['href']
                catUrl = f'{baseUrl}{href}?page={page}'
                print(catUrl)
                try:
                    cathtml = urlopen(catUrl).read()
                    catSoup = BeautifulSoup(cathtml, features = 'html.parser')
                    catName = catSoup.find('h1', class_ = 'search-title').text.strip()
                    items = catSoup.find_all('div', class_ = 'tovar__item')
                    for item in items:
                        if 'slick-slide' not in item.attrs['class']:
                            price = item.find('span', class_ = 'price__real').text.strip()
                            np = item.find('span', class_ = 'price__past')
                            if np:
                                np = np.text.strip()
                            else:
                                np = price
                            name = item.find('h3', class_ = 'tovar__name').text.strip()
                            if name:
                                writer.writerow([catName, page, name, price, np, current_datetime])
                    paging = catSoup.find_all('a', class_ = 'pag__item', href = True)
                    if paging:
                        lastPage = paging[-1].find('span').text
                        if lastPage.isdigit():
                            hasMorePages = int(lastPage) > page
                        else:
                            hasMorePages = False
                    else:
                        hasMorePages = False
                    page += 1
                except:
                    hasMorePages = False
                    print("An exception occurred")
                