import pandas as pd
from bs4 import BeautifulSoup
import requests

number_of_pages = 2


def get_page_data(page_no):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }

    r = requests.get(
        'https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_' + str(
            page_no) + '?_encoding=UTF8&pg=' + str(page_no),
        headers=headers)  # , proxies=proxies)
    resp_text = r.text
    soup = BeautifulSoup(resp_text, 'lxml')

    books = []
    for d in soup.find_all('div', attrs={'class': 'a-section a-spacing-none aok-relative'}):
        book_info = d.find('div', attrs={'class': 'a-section a-spacing-small'}).find('img')
        name = book_info['alt']
        author = d.find('a', attrs={'class': 'a-size-small a-link-child'})
        rating = d.find('span', attrs={'class': 'a-icon-alt'})
        number_of_ratings = d.find('a', attrs={'class': 'a-size-small a-link-normal'})
        price = d.find('span', attrs={'class': 'p13n-sc-price'})
        photo = book_info['src']

        book = []

        if name is not None:
            book.append(name)
        else:
            book.append("Unknown Book")

        if author is not None:
            book.append(author.text)
        elif author is None:
            author = d.find('span', attrs={'class': 'a-size-small a-color-base'})
            if author is not None:
                book.append(author.text)
            else:
                book.append('Unknown Author')

        if rating is not None:
            # print(rating.text)
            book.append(rating.text)
        else:
            book.append('Unknown Rating')

        if number_of_ratings is not None:
            # print(price.text)
            book.append(number_of_ratings.text)
        else:
            book.append('0')

        if price is not None:
            # print(price.text)
            book.append(price.text)
        else:
            book.append('Unknown Price')

        if photo is not None:
            book.append(photo)
        else:
            book.append("No Photo Available")

        books.append(book)
    return books


results = []
for page in range(1, number_of_pages + 1):
    results.append(get_page_data(page))
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results), columns=['Book Name', 'Author', 'Rating', 'Number_Of_Ratings', 'Price', 'Photo'])
df.to_csv('amazon_best_selling_books.csv', index=False, encoding='utf-8')