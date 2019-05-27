import requests
from bs4 import BeautifulSoup
import re


def get_html(url):
    r = requests.get(url)

    return r.text


def get_promos(html):
    soup = BeautifulSoup(html, 'lxml')
    promo_list = soup.find('ul', class_='promo_list promo_type2')
    promos = promo_list.find_all('li')

    return promos


def parse_promos(promos):
    for promo in promos:
        picture = 'https://www.atbmarket.com/' + promo.find('img').get('src')

        info = re.sub(r'</?.*?>', '', str(promo.find('span', class_='promo_info_text'))).strip().split('\n')
        info = ' '.join(list(map(lambda i: i.strip(), info)))

        price = str(promo.find('div', class_='promo_price')).split('<span>')
        price = price[0][25:] + '.' + price[1][:2] + ' ₴'

        yield picture, info, price


def get_parsed_atb():
    html = get_html('https://www.atbmarket.com/ru/hot/akcii/economy/')
    promos = get_promos(html)
    result = list(parse_promos(promos))

    return result


if __name__ == '__main__':
    parsed = get_parsed_atb()
    # for i in parsed:
    #     print(i)

    with open('../discounts/atb_discounts.py', 'w') as atb_discounts:
        atb_discounts.write('discounts = {}'.format(parsed))