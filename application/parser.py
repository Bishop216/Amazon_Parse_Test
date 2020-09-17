from bs4 import BeautifulSoup


def parse_product(product_html, all_reviews_html, pos_reviews_html):
    # Product page
    product_page_soup = BeautifulSoup(product_html.content, 'html.parser')

    name = product_page_soup.find(id='productTitle').string.strip()
    ratings = int(product_page_soup.find(id='acrCustomerReviewText').string.split(" ")[0].replace(',', ''))
    avg_rating = float(product_page_soup.find('span', attrs={'data-hook': 'rating-out-of-text'}).string.split(' ')[0])
    answered_questions_number = product_page_soup.find(id='askATFLink').find('span', attrs={'class': 'a-size-base'}) \
        .string.strip().split(' ')[0]

    # All reviews page
    all_reviews_page_soup = BeautifulSoup(all_reviews_html.content, 'html.parser')

    review_number = int(
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
        'avg_rating': avg_rating,
        'review_number': review_number,
        'positive_review_number': positive_review_number,
        'answered_questions_number': answered_questions_number
    }

    return product_info
