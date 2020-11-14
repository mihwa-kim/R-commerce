import requests
from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
import schedule
import time
import pandas as pd

client = MongoClient('localhost', 27017)
db = client.dbcuration

app = Flask(__name__)

driver = webdriver.Chrome('C:/Users/user/Desktop/chromedriver')
driver.implicitly_wait(20)

deals = list(db.deals.find({},{'url': 1, '_id':0}))



for deal in deals:
    url = deal['url']

    url_list = 'https://www.coupang.com' + str(url)

    driver.get(url_list)
    time.sleep(20)

    # req = driver.page_source
    #
    # print(req)

    # print(driver.page_source)

    reviews = driver.find_elements_by_class_name('product-review')

    for value in reviews:
        print(value.text)

    # reviews_data = reviews.text
    # print(reviews_data)

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    # data = requests.get(url_list, headers=headers)

    # soup = BeautifulSoup(req, 'html.parser')
    # print(soup)
    # reviews = soup.select('.sdp-review__highlight__positive')
    # # reviews = list(soup.select('#btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer'))
    # # btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__highlight.js_reviewHighLightContainer
    #
    # # btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__highlight.js_reviewHighLightContainer > article.sdp-review__highlight__positive
    #
    # # '#btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer'
    # print(reviews)






    # for count, review in enumerate(reviews):
    #     title = list(review.select_one(' div.sdp-review__article__list__info > div.sdp-review__article__list__info__product-info__name').text)
    #     comment = list(review.select_one('div.sdp-review__article__list__review.js_reviewArticleContentContainer > div').text)
    #     star = list(review.select_one('.data-rating'))
    #     print(title, comment, star)
    #
    #     if count == 5:
    #         break

    break

# driver.close()

#btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > article:nth-child(3)
#btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > article:nth-child(3)
#btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > article:nth-child(7) > div.sdp-review__article__list__info > div.sdp-review__article__list__info__product-info > div.sdp-review__article__list__info__product-info__star-gray > div
#btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > article:nth-child(5) > div.sdp-review__article__list__review.js_reviewArticleContentContainer > div
#btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > article:nth-child(3) > div.sdp-review__article__list__review.js_reviewArticleContentContainer > div
#btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > article:nth-child(3) > div.sdp-review__article__list__info > div.sdp-review__article__list__info__product-info__name

