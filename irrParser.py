import requests
import re
from bs4 import BeautifulSoup


class Ground:
    name = ""
    url = ""

    def __init__(self, name, url):
        self.name = name
        self.url = url


url = 'http://kazan.irr.ru/real-estate/out-of-town/lands/'
irr = []
new_request = requests.get(url)
soup = BeautifulSoup(new_request.content, 'html.parser')
last_page = int(soup.findAll('a', {'class': 'pagination__pagesLink'})[-1].text)

for i in range(last_page):
    new_request = requests.get(url+"page"+str(i+1))
    soup = BeautifulSoup(new_request.content, 'html.parser')
    clear_data = soup.findAll('a', {'class': 'listing__itemTitle js-productListingProductName'})
    for j in range(clear_data.__len__()):
        irr.append(Ground(clear_data[j].text, clear_data[j]['href']))

for i in irr:
    print(i.name + " " + i.url)
