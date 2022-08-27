import requests
import webbrowser as wb
import regex as re
from bs4 import BeautifulSoup
import pandas as pd

cities = ['sanmarcos', 'sanantonio', 'austin', 'collegestation', 'corpuschristi',
          'houston', 'killeen', 'sanangelo', 'victoriatx']
urls = [f'https://{city}.craigslist.org/search/cta?purveyor=owner' for city in cities]

max_pages = {}

for url in urls:
    counts = []
    response = requests.get(url)
    for elem in re.split('totalcount">|</span>', response.text):
        if elem.isdigit():
            counts.append(elem)

    max_pages[url] = int(counts[0])    


every_url = []
for key, value in max_pages.items():
    full_pages = int(value / 120)
    remainder = value - (value % 120)
    every_url.append(key)
    [every_url.append(key+f'&s={x * 120}') for x in range(1, full_pages)]
    if remainder != value and remainder:
        every_url.append(key+f'?={remainder}')

for url in every_url:

    soup = requests.get(url)
    soup = BeautifulSoup(soup.text, 'html.parser')

    a_result = soup.find_all('li', class_="result-row")[0]

    all_results = soup.find_all('li', class_="result-row")
    #print(str(a_result))

    car_listings = []
    for result in all_results:
        
        car_dict = {}
        title = re.split('<a class="result-title hdrlnk" data-id=|</a>', str(result))[2]

        car_dict['posting_url'] = (title.split('href=')[1]).split(' id="')[0][1:-1]
        car_dict['post_title'] = title.split('>')[1]
        car_dict['price'] = re.split('class="result-price">\$|</span>', str(result))[1]

        car_listings.append(car_dict)

    df = pd.DataFrame(car_listings)
    df.to_csv(f'car_csvs/{url[8:17] + url[-3:]}.csv', index=False)