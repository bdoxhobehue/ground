import requests
import time
from bs4 import BeautifulSoup
import codecs


class Ground:
    name = ""
    url = ""
    description = ""
    cost = 0

    def __init__(self, name, url):
        self.name = name
        self.url = url


def find_distance(origin, destination):
    KEY = "AIzaSyBSJywKPIK1ONXOByLvjPHeqvNhIFd6Cu4"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origin + "&destinations=" + destination + "&mode=walking&language=EN&key=" + KEY
    response = requests.get(url)
    json = response.json()
    return int(json['rows'][0]['elements'][0]['distance']['value'])

timeStart = time.time();
url = 'http://kazan.irr.ru/real-estate/out-of-town/lands/'
print("Searching page", url)
baseOfProposals = []
new_request = requests.get(url)
soup = BeautifulSoup(new_request.content, 'html.parser')
last_page = int(soup.findAll('a', {'class': 'pagination__pagesLink'})[-1].text)
print("Total count of pages is :{0}".format(last_page))
print("Starting adding all references to the Ground class instance")

for i in range(last_page):
    new_request = requests.get(url + "page" + str(i + 1))
    soup = BeautifulSoup(new_request.content, 'html.parser')
    clear_data = soup.findAll('a', {'class': 'listing__itemTitle js-productListingProductName'})
    for j in range(clear_data.__len__()):
        baseOfProposals.append(Ground(clear_data[j].text, clear_data[j]['href']))
    print("Complete: {:.2%}".format(i/last_page))


print("Successfully created ground objects with name and urls")
print("in {:.3} sec:".format(time.time() - timeStart))

timeStart = time.time()
counter = 0

print("\n\n\n")
print("Starting base filling")

for i in baseOfProposals:
    counter=counter+1
    new_request = requests.get(i.url)
    soup = BeautifulSoup(new_request.content, 'html.parser')
    i.cost = soup.findAll('div', {'class': 'productPage__price js-contentPrice'})[0]['content']
    i.description = soup.findAll('p', {'class': 'productPage__descriptionText js-productPageDescription'})[0].text
    print(counter)
    print("Complete: {:.2%}".format(counter/len(baseOfProposals)))

print("Time elapsed: {:.4} ".format(time.time() - timeStart))

with codecs.open("output.txt", 'w', 'UTF-8') as outputfile:
    counter = 0
    for i in baseOfProposals:
        counter = counter + 1
        outputfile.write("{4} Name: {0}  URL: {1} Cost: {2} Description:{3} \n".format(i.name, i.url, str(i.cost), i.description, counter))