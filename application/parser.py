import io
import requests
import csv

from flask import request, Blueprint, jsonify
from bs4 import BeautifulSoup

import application.local as local
import application.config as config

from application.models import db, Asins, ProductInfo, Reviews

bp = Blueprint('parser', __name__, url_prefix='/parser')


def parse_product(product_html, all_reviews_html, pos_reviews_html):
    """
    Parses html pages and retrieves needed product information.

    Amazon changed the layout of the product review page
    so you cannot get the number of all/positive/critical reviews from the same page.
    You have do it separately providing a query parameter in the url
    (?&filterByStar=all_stars/positive/critical).

    :param product_html:
    :param all_reviews_html:
    :param pos_reviews_html:
    :return:
    """
    # Product page
    product_page_soup = BeautifulSoup(product_html.content, 'html.parser')

    name = product_page_soup.find(id='productTitle').string.strip()
    ratings = int(product_page_soup.find(id='acrCustomerReviewText').string.split(" ")[0].replace(',', ''))
    avg_rating = float(product_page_soup.find('span', attrs={'data-hook': 'rating-out-of-text'}).string.split(' ')[0])
    answered_questions_number = product_page_soup.find(id='askATFLink').find('span', attrs={'class': 'a-size-base'}) \
        .string.strip().split(' ')[0]

    # All reviews page
    all_reviews_page_soup = BeautifulSoup(all_reviews_html.content, 'html.parser')

    reviews_number = int(
        all_reviews_page_soup.find('div', attrs={'data-hook': 'cr-filter-info-review-rating-count'}).find('span')
            .string.strip().split('|')[1].strip().split(' ')[0].replace(',', ''))

    # Positive reviews page
    positive_reviews_page_soup = BeautifulSoup(pos_reviews_html.content, 'html.parser')

    positive_review_number = int(
        positive_reviews_page_soup.find('div', attrs={'data-hook': 'cr-filter-info-review-rating-count'}).find('span')
            .string.strip().split('|')[1].strip().split(' ')[0].replace(',', ''))

    product_info = {
        'name': name,
        'ratings': ratings,
        'average_rating': avg_rating,
        'reviews_number': reviews_number,
        'positive_review_number': positive_review_number,
        'answered_questions_number': answered_questions_number
    }

    return product_info


def allowed_file(filename):
    """
    Checks if file type id correct.
    :param filename:
    :return bool:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'csv'


@bp.route('/upload', methods=['POST'])
def receive_csv():
    """

    :return:
    """
    if 'file' not in request.files:
        return jsonify(message='No file provided.'), 400

    file = request.files['file']

    if file and allowed_file(file.filename):
        file_content = io.StringIO(file.stream.read().decode('UTF8'))
        reader = csv.reader(file_content)

        asins = set()
        for row in reader:
            asins.update(row)

        asins = list(asins)
        for asin in asins:
            product_url = config.product_url.format(asin)
            product_all_reviews_url = config.product_all_reviews_url.format(asin)
            product_positive_reviews_url = config.product_positive_reviews_url.format(asin)

            product_page = requests.get('https://app.zenscrape.com/api/v1/get',
                                        headers=local.z_header,
                                        params=('url', product_url))

            all_reviews_page = requests.get('https://app.zenscrape.com/api/v1/get',
                                            headers=local.z_header,
                                            params=('url', product_all_reviews_url))

            positive_reviews_page = requests.get('https://app.zenscrape.com/api/v1/get',
                                                 headers=local.z_header,
                                                 params=('url', product_positive_reviews_url))

            try:
                product_info = parse_product(product_page,
                                             all_reviews_page,
                                             positive_reviews_page)
            except Exception as e:
                return jsonify(message='Something went wrong.'), 400

            asin_obj = Asins(id=asin)
            db.session.add(asin_obj)

            product_info_obj = ProductInfo(asin_id=asin,
                                           name=product_info['name'],
                                           ratings=product_info['ratings'],
                                           average_rating=product_info['average_rating'])
            db.session.add(product_info_obj)

            review_obj = Reviews(asin_id=asin,
                                 reviews_number=product_info['review_number'],
                                 positive_reviews_number=product_info['positive_review_number'],
                                 answered_questions_number=product_info['answered_questions_number'])
            db.session.add(review_obj)

            db.session.commit()

        return jsonify(message='success')

    return jsonify({"message": "Incorrect file type."}), 400
