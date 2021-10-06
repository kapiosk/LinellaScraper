#!venv/bin python3
# -*- coding: utf-8 -*-

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

baseUrl = 'https://linella.md'

html = urlopen(baseUrl+'/en').read()
# html = html.decode('utf-8')

soup = BeautifulSoup(html, features='html.parser')
generalCategories = soup.find_all('ul', class_='level2')

header = ['category', 'page', 'name', 'price']

with open('items.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for gc in generalCategories:
        categories = gc.find_all('a', href=True)
        for category in categories:
            hasItems = True
            page = 1
            #while hasItems:
            href = category['href']
            catUrl = f'{baseUrl}{href}?page={page}'
            print(catUrl)
            try:
                cathtml = urlopen(catUrl).read()
                # cathtml = cathtml.decode('utf-8')
                catSoup = BeautifulSoup(cathtml, features='html.parser')
                catName = catSoup.find('h1', class_='search-title').text.strip()
                items = catSoup.find_all('div', class_='tovar__item')
                for item in items:
                    if 'slick-slide' not in item.attrs['class']:
                        price = item.find('span', class_='price__real').text.strip()
                        name = item.find('h3', class_='tovar__name').text.strip()
                        if name:
                            writer.writerow([catName, page, name, price])
                        #hasItems = False
                #hasItems = False #not hasItems
                page += 1
            except:
                print("An exception occurred")

                