import requests
from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
from pymongo import MongoClient
import schedule

client = MongoClient('localhost', 27017)
db = client.dbcuration


def craw_page(url, keyword, color, gender):
    print("======= Crawling data...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    deals = list(soup.select('.search-product'))

    for deal in deals:
        a_tag = deal.select_one('a')
        if a_tag is not None:
            id = deal['id']

            image_tag = deal.select_one('dl > dt > img')['src']
            # \32 249280097 > a > dl > dt > img
            # \32 01865926 > a > dl > dt > img
            if image_tag == '//img1a.coupangcdn.com/image/coupang/search/blank1x1.gif':

                image = deal.select_one('dl > dt > img')['data-img-src']

            else:
                image = deal.select_one('dl > dt > img')['src']


            url = deal.select_one('.search-product-link')['href']
            # \32 264407365 > a
            title = deal.select_one('dl > dd > div > div.name').text
            # \32 307713853 > a > dl > dd > div > div.name
            # \32 332785161 > a > dl > dd > div > div.name
            price = deal.select_one('.price-value').text

            rating_tag = deal.select_one('.rating')
            if rating_tag:
                star = rating_tag.text
            else:
                star = '0'

            free_shipping_tag = deal.select_one('dl > dd > div.badges > span')
            if free_shipping_tag:
                shipping = 'free'
            else:
                shipping = 'not free'

            # products.append({'id': id, 'image': image, 'url': url, 'title': title, 'price': price})

            doc = {
                'gender': gender,
                'keyword': keyword,
                'color': color,
                'id': id,
                'image': image,
                'url': url,
                'title': title,
                'price': price,
                'star': star,
                'shipping': shipping,

            }

            db.deals.insert_one(doc)

    print("======= Crawling data finished!")


def clean_db():
    print("======= Cleaning DB...")
    db.deals.drop()
    print("======= Cleaning DB Finished...")


def job_at_everyday_1am():
    clean_db()

    woman = {
        'business_url': {
            'black': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244278%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'grey': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244280%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'navy': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244279%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'silver': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244281%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'red': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244282%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'orange': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244283%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'yellow': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244284%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'green': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244285%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'violet': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244287%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'white': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244289%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'beige': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244292%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'brown': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244290%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
        }
    }

    man = {
        'business_url': {
            'black': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244278%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'grey': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244280%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'navy': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244279%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'silver': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244281%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'red': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244282%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'orange': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244283%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'yellow': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244284%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'green': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244285%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'violet': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244287%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'white': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244289%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'beige': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244292%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'brown': 'https://www.coupang.com/np/search?q=%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244290%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
        }
    }

    craw_page(woman['business_url']['black'], 'business', 'black', 'woman')
    craw_page(woman['business_url']['grey'], 'business', 'grey', 'woman')
    craw_page(woman['business_url']['navy'], 'business', 'navy', 'woman')
    craw_page(woman['business_url']['silver'], 'business', 'silver', 'woman')
    craw_page(woman['business_url']['red'], 'business', 'red', 'woman')
    craw_page(woman['business_url']['orange'], 'business', 'orange', 'woman')
    craw_page(woman['business_url']['yellow'], 'business', 'yellow', 'woman')
    craw_page(woman['business_url']['green'], 'business', 'green', 'woman')
    craw_page(woman['business_url']['violet'], 'business', 'violet', 'woman')
    craw_page(woman['business_url']['white'], 'business', 'white', 'woman')
    craw_page(woman['business_url']['beige'], 'business', 'beige', 'woman')
    craw_page(woman['business_url']['brown'], 'business', 'brown', 'woman')

    craw_page(man['business_url']['black'], 'business', 'black', 'man')
    craw_page(man['business_url']['grey'], 'business', 'grey', 'man')
    craw_page(man['business_url']['navy'], 'business', 'navy', 'man')
    craw_page(man['business_url']['silver'], 'business', 'silver', 'man')
    craw_page(man['business_url']['red'], 'business', 'red', 'man')
    craw_page(man['business_url']['orange'], 'business', 'orange', 'man')
    craw_page(man['business_url']['yellow'], 'business', 'yellow', 'man')
    craw_page(man['business_url']['green'], 'business', 'green', 'man')
    craw_page(man['business_url']['violet'], 'business', 'violet', 'man')
    craw_page(man['business_url']['white'], 'business', 'white', 'man')
    craw_page(man['business_url']['beige'], 'business', 'beige', 'man')
    craw_page(man['business_url']['brown'], 'business', 'brown', 'man')

    woman = {
        'casual_url': {
            'black': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244278%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'grey': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244280%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'navy': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244279%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'silver': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244281%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'red': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244282%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'orange': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244283%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'yellow': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244284%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'green': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244285%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'violet': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244287%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'white': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244289%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'beige': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244292%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'brown': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244290%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
        }
    }

    man = {
        'casual_url': {
            'black': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244278%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'grey': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244280%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'navy': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244279%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'silver': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244281%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'red': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244282%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'orange': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244283%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'yellow': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244284%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'green': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244285%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'violet': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244287%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'white': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244289%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'beige': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244292%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'brown': 'https://www.coupang.com/np/search?q=%EC%BA%90%EC%A3%BC%EC%96%BC%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244290%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
        }
    }

    craw_page(woman['casual_url']['black'], 'casual', 'black', 'woman')
    craw_page(woman['casual_url']['grey'], 'casual', 'grey', 'woman')
    craw_page(woman['casual_url']['navy'], 'casual', 'navy', 'woman')
    craw_page(woman['casual_url']['silver'], 'casual', 'silver', 'woman')
    craw_page(woman['casual_url']['red'], 'casual', 'red', 'woman')
    craw_page(woman['casual_url']['orange'], 'casual', 'orange', 'woman')
    craw_page(woman['casual_url']['yellow'], 'casual', 'yellow', 'woman')
    craw_page(woman['casual_url']['green'], 'casual', 'green', 'woman')
    craw_page(woman['casual_url']['violet'], 'casual', 'violet', 'woman')
    craw_page(woman['casual_url']['white'], 'casual', 'white', 'woman')
    craw_page(woman['casual_url']['beige'], 'casual', 'beige', 'woman')
    craw_page(woman['casual_url']['brown'], 'casual', 'brown', 'woman')

    craw_page(man['casual_url']['black'], 'casual', 'black', 'man')
    craw_page(man['casual_url']['grey'], 'casual', 'grey', 'man')
    craw_page(man['casual_url']['navy'], 'casual', 'navy', 'man')
    craw_page(man['casual_url']['silver'], 'casual', 'silver', 'man')
    craw_page(man['casual_url']['red'], 'casual', 'red', 'man')
    craw_page(man['casual_url']['orange'], 'casual', 'orange', 'man')
    craw_page(man['casual_url']['yellow'], 'casual', 'yellow', 'man')
    craw_page(man['casual_url']['green'], 'casual', 'green', 'man')
    craw_page(man['casual_url']['violet'], 'casual', 'violet', 'man')
    craw_page(man['casual_url']['white'], 'casual', 'white', 'man')
    craw_page(man['casual_url']['beige'], 'casual', 'beige', 'man')
    craw_page(man['casual_url']['brown'], 'casual', 'brown', 'man')

    woman = {
        'training_url': {
            'black': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244278%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'grey': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244280%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'navy': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244279%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'silver': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244281%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'red': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244282%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'orange': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244283%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'yellow': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244284%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'green': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244285%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'violet': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244287%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'white': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244289%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'beige': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244292%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'brown': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244290%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
        }
    }

    man = {
        'training_url': {
            'black': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244278%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'grey': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244280%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'navy': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244279%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'silver': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244281%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'red': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244282%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'orange': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244283%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'yellow': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244284%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'green': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244285%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'violet': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244287%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'white': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244289%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'beige': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244292%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'brown': 'https://www.coupang.com/np/search?q=%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%8B%9D&brand=&offerCondition=&filter=1%23attr_10496%244290%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
        }
    }

    craw_page(woman['training_url']['black'], 'training', 'black', 'woman')
    craw_page(woman['training_url']['grey'], 'training', 'grey', 'woman')
    craw_page(woman['training_url']['navy'], 'training', 'navy', 'woman')
    craw_page(woman['training_url']['silver'], 'training', 'silver', 'woman')
    craw_page(woman['training_url']['red'], 'training', 'red', 'woman')
    craw_page(woman['training_url']['orange'], 'training', 'orange', 'woman')
    craw_page(woman['training_url']['yellow'], 'training', 'yellow', 'woman')
    craw_page(woman['training_url']['green'], 'training', 'green', 'woman')
    craw_page(woman['training_url']['violet'], 'training', 'violet', 'woman')
    craw_page(woman['training_url']['white'], 'training', 'white', 'woman')
    craw_page(woman['training_url']['beige'], 'training', 'beige', 'woman')
    craw_page(woman['training_url']['brown'], 'training', 'brown', 'woman')

    craw_page(man['training_url']['black'], 'training', 'black', 'man')
    craw_page(man['training_url']['grey'], 'training', 'grey', 'man')
    craw_page(man['training_url']['navy'], 'training', 'navy', 'man')
    craw_page(man['training_url']['silver'], 'training', 'silver', 'man')
    craw_page(man['training_url']['red'], 'training', 'red', 'man')
    craw_page(man['training_url']['orange'], 'training', 'orange', 'man')
    craw_page(man['training_url']['yellow'], 'training', 'yellow', 'man')
    craw_page(man['training_url']['green'], 'training', 'green', 'man')
    craw_page(man['training_url']['violet'], 'training', 'violet', 'man')
    craw_page(man['training_url']['white'], 'training', 'white', 'man')
    craw_page(man['training_url']['beige'], 'training', 'beige', 'man')
    craw_page(man['training_url']['brown'], 'training', 'brown', 'man')

    woman = {
        'date_url': {
            'black': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244278%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'grey': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244280%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'navy': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244279%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'silver': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244281%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'red': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244282%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'orange': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244283%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'yellow': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244284%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'green': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244285%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'violet': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244287%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'white': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244289%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'beige': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244292%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'brown': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244290%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
        }
    }

    man = {
        'date_url': {
            'black': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244278%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'grey': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244280%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'navy': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244279%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'silver': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244281%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'red': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244282%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'orange': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244283%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'yellow': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244284%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'green': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244285%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'violet': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244287%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'white': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244289%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'beige': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244292%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'brown': 'https://www.coupang.com/np/search?q=%EC%86%8C%EA%B0%9C%ED%8C%85%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244290%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
        }
    }

    craw_page(woman['date_url']['black'], 'date', 'black', 'woman')
    craw_page(woman['date_url']['grey'], 'date', 'grey', 'woman')
    craw_page(woman['date_url']['navy'], 'date', 'navy', 'woman')
    craw_page(woman['date_url']['silver'], 'date', 'silver', 'woman')
    craw_page(woman['date_url']['red'], 'date', 'red', 'woman')
    craw_page(woman['date_url']['orange'], 'date', 'orange', 'woman')
    craw_page(woman['date_url']['yellow'], 'date', 'yellow', 'woman')
    craw_page(woman['date_url']['green'], 'date', 'green', 'woman')
    craw_page(woman['date_url']['violet'], 'date', 'violet', 'woman')
    craw_page(woman['date_url']['white'], 'date', 'white', 'woman')
    craw_page(woman['date_url']['beige'], 'date', 'beige', 'woman')
    craw_page(woman['date_url']['brown'], 'date', 'brown', 'woman')

    craw_page(man['date_url']['black'], 'date', 'black', 'man')
    craw_page(man['date_url']['grey'], 'date', 'grey', 'man')
    craw_page(man['date_url']['navy'], 'date', 'navy', 'man')
    craw_page(man['date_url']['silver'], 'date', 'silver', 'man')
    craw_page(man['date_url']['red'], 'date', 'red', 'man')
    craw_page(man['date_url']['orange'], 'date', 'orange', 'man')
    craw_page(man['date_url']['yellow'], 'date', 'yellow', 'man')
    craw_page(man['date_url']['green'], 'date', 'green', 'man')
    craw_page(man['date_url']['violet'], 'date', 'violet', 'man')
    craw_page(man['date_url']['white'], 'date', 'white', 'man')
    craw_page(man['date_url']['beige'], 'date', 'beige', 'man')
    craw_page(man['date_url']['brown'], 'date', 'brown', 'man')
    # craw_page(casual_url['black'], 'casual', 'black')

    woman = {
        'travel_url': {
            'black': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244278%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'grey': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244280%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'navy': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244279%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'silver': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244281%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'red': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244282%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'orange': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244283%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'yellow': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244284%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'green': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244285%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'violet': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244287%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'white': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244289%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'beige': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244292%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
            'brown': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244290%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186664&rating=0&sorter=saleCountDesc&listSize=36',
        }
    }
    man = {
        'travel_url': {
            'black': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244278%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'grey': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244280%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'navy': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244279%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'silver': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244281%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'red': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244282%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'orange': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244283%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'yellow': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244284%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'green': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244285%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'violet': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244287%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'white': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244289%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'beige': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244292%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
            'brown': 'https://www.coupang.com/np/search?q=%EB%B0%94%EC%BA%89%EC%8A%A4%EB%A3%A9&brand=&offerCondition=&filter=1%23attr_10496%244290%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&component=186969&rating=0&sorter=saleCountDesc&listSize=36',
        }
    }

    craw_page(woman['travel_url']['black'], 'travel', 'black', 'woman')
    craw_page(woman['travel_url']['grey'], 'travel', 'grey', 'woman')
    craw_page(woman['travel_url']['navy'], 'travel', 'navy', 'woman')
    craw_page(woman['travel_url']['silver'], 'travel', 'silver', 'woman')
    craw_page(woman['travel_url']['red'], 'travel', 'red', 'woman')
    craw_page(woman['travel_url']['orange'], 'travel', 'orange', 'woman')
    craw_page(woman['travel_url']['yellow'], 'travel', 'yellow', 'woman')
    craw_page(woman['travel_url']['green'], 'travel', 'green', 'woman')
    craw_page(woman['travel_url']['violet'], 'travel', 'violet', 'woman')
    craw_page(woman['travel_url']['white'], 'travel', 'white', 'woman')
    craw_page(woman['travel_url']['beige'], 'travel', 'beige', 'woman')
    craw_page(woman['travel_url']['brown'], 'travel', 'brown', 'woman')

    craw_page(man['travel_url']['black'], 'travel', 'black', 'man')
    craw_page(man['travel_url']['grey'], 'travel', 'grey', 'man')
    craw_page(man['travel_url']['navy'], 'travel', 'navy', 'man')
    craw_page(man['travel_url']['silver'], 'travel', 'silver', 'man')
    craw_page(man['travel_url']['red'], 'travel', 'red', 'man')
    craw_page(man['travel_url']['orange'], 'travel', 'orange', 'man')
    craw_page(man['travel_url']['yellow'], 'travel', 'yellow', 'man')
    craw_page(man['travel_url']['green'], 'travel', 'green', 'man')
    craw_page(man['travel_url']['violet'], 'travel', 'violet', 'man')
    craw_page(man['travel_url']['white'], 'travel', 'white', 'man')
    craw_page(man['travel_url']['beige'], 'travel', 'beige', 'man')
    craw_page(man['travel_url']['brown'], 'travel', 'brown', 'man')
