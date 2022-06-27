import requests
from bs4 import BeautifulSoup

from shop_project.shop.models import Product
from shop_project.shop_project.settings import URL_SCRAPING_DOMAIN, URL_SCRAPING_ELECTRIC

"""
{
    'name': 'Труба профильная 40х20 2 мм 3м', 
    'image_url': 'https://my-website.com/30C39890-D527-427E-B573-504969456BF5.jpg', 
    'price': Decimal('493.00'), 
    'unit': 'за шт', 
    'code': '38140012'
 }
"""


class ScrapingError(Exception):
    pass


class ScrapingTimeoutError(ScrapingError):
    pass


class ScrapingHTTPError(ScrapingError):
    pass


class ScrapingOtherError(ScrapingError):
    pass


def scraping_electric():
    try:
        resp = requests.get(URL_SCRAPING_ELECTRIC, timeout=10.0)
    except requests.exceptions.Timeout:
        raise ScrapingTimeoutError("request timed out")
    except Exception as e:
        raise ScrapingOtherError(f'{e}')

    if resp.status_code != 200:
        raise ScrapingHTTPError(f"HTTP {resp.status_code}: {resp.text}")

    data_list = []
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    all_pics = soup.find_all('img', {'class': 'img-responsive', 'itemprop': "image"})
    all_prices = soup.find_all('meta', itemprop="price")
    all_details = soup.find_all('a', {'itemprop': 'image', 'itemtype': "http://schema.org/ImageObject"})
    all_codes = soup.find_all('a', class_='add-to-fav')
    for item in range(len(all_pics)):
        data = {}
        name = all_pics[item].get('title')
        data['name'] = name
        price = int(all_prices[item].get('content'))
        data['price'] = price
        img_url = all_pics[item].get('data-src')
        data['img_url'] = img_url
        detail_url = all_details[item].get('href')
        data['detail_url'] = f'{URL_SCRAPING_DOMAIN}{detail_url}'
        code = all_codes[item].get('data-id-favorites')
        data['code'] = code
        data_list.append(data)

        print(data)

    for item in data_list:
        if not Product.objects.filter(code=item['code']).exists():
            Product.objects.create(
                name=item['name'],
                code=item['code'],
                price=item['price'],
                unit=item['unit'],
                image_url=item['image_url'],
            )

    return data_list


if __name__ == '__main__':
    scraping_electric()
