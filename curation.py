import requests
from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
from pymongo import MongoClient
# from selenium import webdriver
import schedule
from jobs import job_at_everyday_1am

client = MongoClient('localhost', 27017)
db = client.dbcuration

app = Flask(__name__)

# driver = webdriver.Chrome("C:/Users/user/Desktop/chromedriver")
# ## HTML을 주는 부분
#
# # ## API 역할을 하는 부분
# @app.route('/', methods=['GET'])
# def home():
#     return render_template('Rcommerce.html')
#
# def get_Reviews():
#
#         target = db.curation.find({},{'_id': 0})
#         target_url = target['url']
#         url = 'https://coupang.com'+target_url
#         driver.get(url)
#
#         req = driver.page_source
#
#         soup = BeautifulSoup(req, 'html.parser')
#
#         reviews = soup.select('btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer')
#     #btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > article:nth-child(3)
#     #btfTab > ul.tab-contents > li.product-review > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > article:nth-child(4)
#         for count, review in enumerate(reviews):
#             review = review.select_one('review')
#             print(review)
#             if count == 10:
#                 break
#
#         driver.close()


# def curation_get():
#     gender_receive = request.args.get('gender_give')
#     tone_receive = request.args.get('tone_give')
#     tpo_receive = request.args.get('tpo_give')
#
#     print(gender_receive, tone_receive, tpo_receive)
#
#     return jsonify({'result': 'success'})

@app.route('/')
def home():
    return render_template('personalcuration.html')

def get_item_list_from_keyword(gender, tone, keyword):
    # { “writer”: { $ in: [ “Alpha”, “Bravo”]}
    # query = db.deals.find({}, {'_id': 0})

    gender_list_set = {
        'woman': ['woman'],
        'man': ['man']
    }

    color_list_set = {
        'spring-warm': ['black', 'navy', 'orange', 'yellow', 'beige', 'brown'],
        'summer-cool': ['black', 'grey', 'navy', 'silver', 'violet', 'white'],
        'autumn-warm': ['black', 'navy', 'red', 'green', 'violet', 'beige', 'brown'],
        'winter-cool': ['black', 'grey', 'navy', 'silver', 'red', 'yellow', 'green', 'violet', 'white'],
    }

    keyword_list_set = {
        'business': ['business'],
        'blind-date': ['date'],
        'meet-friends': ['casual'],
        'school': ['casual', 'training'],
        'traveling': ['travel'],
    }

    query = db.deals.find(
        {
            'gender': {'$in': gender_list_set[gender]},
            'color': {'$in': color_list_set[tone]},
            'keyword': {'$in': keyword_list_set[keyword]}
        }, {'_id': 0}
    )

    return list(query)


# [{"price": "12,900", ...}]
@app.route('/curation/show', methods=['GET'])
def read_pages():
    gender_receive = request.args.get('gender_give')
    tone_receive = request.args.get('tone_give')
    keyword_receive = request.args.get('keyword_give')

    products = get_item_list_from_keyword(gender_receive, tone_receive, keyword_receive)

    # print("image = {}, url = {}, title = {}, price = {}".format(image, url, title, price))
    return jsonify({'result': 'success', 'products': products})


def run():
    schedule.every().day.at('01:00').do(job_at_everyday_1am) # 매일 09:00 마다 job 함수를 실행
    while True:
        print("WHY")
        schedule.run_pending()


#  schedule.every().day.at('01:00').do(job_at_everyday_1am())  # 매일 09:00 마다 job 함수를 실행
# while True:
#    schedule.run_pending()

print("HERE!!")
if __name__ == '__main__':
    job_at_everyday_1am()
    app.run('0.0.0.0', port=5000, debug=True)
    print('adsasdf')
    # run()
