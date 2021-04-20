import requests
from bs4 import BeautifulSoup
import pandas as pd


url= 'https://auto.ru/moskva/motorcycle/all/?moto_type=SPORTTOURISM&moto_type=SUPERSPORT&moto_type=SPORTBIKE&moto_type=SPORT_GROUP&sort=price-asc'

global hrefs
hrefs = []
title = []
products = []


def getHtml(url,i):
    'Получение HTML'
    global hrefs

    if i>1:
        hrefs = []
        url = 'https://auto.ru/moskva/motorcycle/all/?moto_type=SPORTTOURISM&moto_type=SUPERSPORT&moto_type=SPORTBIKE&moto_type=SPORT_GROUP&page=' + str(i) + '&sort=price-asc'

    r = requests.get(url)
    return r.content.decode('utf-8')



def mount():
    'Получения количества страниц с товарами'
    content = BeautifulSoup(getHtml(url,0))
    return int(content.find_all('span', class_="Button__text")[-4].text)


def allPage(html):
    'Получение ссылок на все товары на странице '
    global hrefs
    content= BeautifulSoup(html)
    pages = content.find_all('a', class_="Link ListingItemTitle-module__link")
    names = content.find_all('a', class_="Link ListingItemTitle-module__link")

    for page in pages:
        hrefs.append(page.get('href'))
    for name in names:
        title.append(name.text)

    return hrefs


def getNormal(text):
    'Удаление лишних элиментов в нужных строках'
    new = text.split('\xa0')
    string=''
    for i in new:
        string+=i
    return string


def getParametrs(hrefs):
    'Получение и запись в массив нужных параметров'
    for i in range(len(hrefs)):
        url = getHtml(hrefs[i],0)
        product = BeautifulSoup(url)
        premileage = product.find('li', class_="CardInfoRow CardInfoRow_kmAge")
        try:
            mileage = premileage .find_all('span', class_ = "CardInfoRow__cell")[1].text

        except:mileage='None'
        place = product.find('span', class_ = "MetroListPlace__regionName MetroListPlace_nbsp").text
        price = product.find('span', class_="OfferPriceCaption__price").text

        products.append([getNormal(price), getNormal(mileage), getNormal(place), hrefs[i]])

    return products


def writeExcel(products):
    'Запись в Excel файл'
    price = []
    mileage = []
    place = []
    hrefs = []

    for i in range(len(products)):
        price.append(products[i][0])
        mileage.append(products[i][1])
        place.append(products[i][2])
        hrefs.append(products[i][3])

    df = pd.DataFrame({'Название': title,
                        'Цена': price,
                        'Пробег': mileage,
                        'Расположение': place,
                        'Ссылки':hrefs})

    df.to_excel('C:\Renata\l.xlsx')


def building(url):
    'Сборка всего функционала'
    global hrefs
    for i in range(1,mount()+1):
        getParametrs(allPage(getHtml(url,i)))

    writeExcel(products)


building(url)
