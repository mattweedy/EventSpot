from bs4 import BeautifulSoup
import requests

html_text = requests.get('').text
soup = BeautifulSoup(html_text, 'lxml')

events = soup.find_all('li', class_='')
for event in events:

    name = soup.find('h2', class_='')
    venue = event.find('p', class_='').text
    date = event.find('p', class_='').text
    price = event.find('p', class_='')

    print(f'''
    Event Name  : {name}
    Event Venue : {venue}
    Event Date  : {date}
    Event Price  : {price}
    ''')

    print('')