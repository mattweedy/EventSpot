from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://www.eventbrite.com/d/ireland--dublin/music--performances/?page=1')

html_text = driver.page_source
soup = BeautifulSoup(html_text, 'lxml')

events = soup.find_all('li', class_='search-main-content__events-list-item search-main-content__events-list-item__mobile')
for event in events:

    name = event.find('h2', class_='Typography_root__4bejd #3a3247 Typography_body-lg__4bejd event-card__clamp-line--two Typography_align-match-parent__4bejd').text
    venue = event.find('p', class_='Typography_root__4bejd #585163 Typography_body-md__4bejd event-card__clamp-line--one Typography_align-match-parent__4bejd').text
    date = event.find('p', class_='Typography_root__4bejd #3a3247 Typography_body-md-bold__4bejd Typography_align-match-parent__4bejd').text
    price = event.find('div', class_='discover-horizontal-event-card__price-wrapper').p.text

    print(f'''
    Event Name  : {name}
    Event Venue : {venue}
    Event Date  : {date}
    Event Price : {price}''')

driver.quit()