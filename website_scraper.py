import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

url = "http://books.toscrape.com/"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

#listing book title, price and rating for all books for all pages
books = []
#we nee to check if there is a next page, if there is we need to go to that page and repeat the process
# we know that the next page is in a ul with class "pager" and the next page link is in a li with class "next"
while True:
    # Find all articles tags with the class "product_pod"
    articles = soup.find_all('article', class_='product_pod')

    for article in articles:
        title = article.h3.a['title']
        price = article.find('p', class_='price_color').text.replace('Â£', '£')
        rating = article.p['class'][1]
        books.append({'title': title, 'price': price, 'rating': rating})

    # Check if there is a next page
    next_page = soup.find('ul', class_='pager').find('li', class_='next')
    if next_page:
        next_page_url = next_page.a['href']
        url = url.rsplit('/', 1)[0] + '/' + next_page_url
        response = requests.get(url)
        time.sleep(0.5) # Add a delay of 0.5 seconds before making the next request to avoid overwhelming the server
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        break # if there is no next page, break the loop

#testing the output
#print(books)
#print(f"Total number of books found: {len(books)}")

# Save the data to a CSV file
df = pd.DataFrame(books)
df.to_csv('books.csv', index=False)

# Save the data to a JSON file
with open('books.json', 'w', encoding='utf-8') as books_file:
    json.dump(books, books_file, indent=2, ensure_ascii=False)