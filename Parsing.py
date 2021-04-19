import requests
from bs4 import BeautifulSoup
import pandas as pd


main='https://auto.ru/moskva/motorcycle/all/?moto_type=SPORTTOURISM&moto_type=SUPERSPORT&moto_type=SPORTBIKE&moto_type=SPORT_GROUP&sort=price-asc'

global links, mount
links = []
call = []
goods = []

def makeUrl(i):
    'Получение ссылок на следующие страницы с товаром'
    main = 'https://auto.ru/moskva/motorcycle/all/?moto_type=SPORTTOURISM&moto_type=SUPERSPORT&moto_type=SPORTBIKE&moto_type=SPORT_GROUP&page='+str(i)+'&sort=price-asc'


def getHtml(main):
    'Получение веб-страницы на текущую страницу'
    r = requests.get(main)
    return r.content.decode('utf-8')


def score():
    'Получения количества страниц с товарами'
    global mount
    all = BeautifulSoup(getHtml(main))
    mount = int(all.find_all('span', class_="Button__text")[-4].text)


def allPage(html):
    'Получение ссылок на все товары на странице '
    global links
    all= BeautifulSoup(html)
    pages = all.find_all('a', class_="Link ListingItemTitle-module__link")
    names = all.find_all('a', class_="Link ListingItemTitle-module__link")

    for page in pages:
        links.append(page.get('href'))
    for name in names:
        call.append(name.text)

    return links


def getNormal(text):
    'Удаление лишних элиментов в нужных строках'
    new = text.split('\xa0')
    string=''
    for i in new:
        string+=i
    return string



def getParametrs(links):
    'Получение и запись в массив нужных параметров'
    for i in range(len(links)):
        url = getHtml(links[i])
        moto = BeautifulSoup(url)
        preludia = moto.find('li', class_="CardInfoRow CardInfoRow_kmAge")
        mileage = preludia.find_all('span', class_ = "CardInfoRow__cell")[1].text
        place = moto.find('span', class_ = "MetroListPlace__regionName MetroListPlace_nbsp").text
        price = moto.find('span', class_="OfferPriceCaption__price").text

        goods.append([getNormal(price),getNormal(mileage),getNormal(place),links[i]])

    return goods


def writeExcel(goods):
    'Запись в Excel файл'
    price = []
    mileage = []
    place = []
    links = []

    for i in range(len(goods)):
        price.append(goods[i][0])
        mileage.append(goods[i][1])
        place.append(goods[i][2])
        links.append(goods[i][3])

    df = pd.DataFrame({'Название': call,
                        'Цена': price,
                        'Пробег': mileage,
                        'Расположение': place,
                        'Ссылки':links})

    df.to_excel('C:\Renata\l.xlsx')


def building(main):
    'Сборка всего функционала'
    global links
    global mount
    score()

    getParametrs(allPage(getHtml(main)))

    for i in range(2,mount+1):
        makeUrl(i)
        links = []
        getParametrs(allPage(getHtml(main)))

    writeExcel(goods)


building(main)
