from bs4 import BeautifulSoup
import requests

# request html from page and create new BeautifulSoup instance using lxml parser
html_text = requests.get('https://www.eventbrite.com/d/ireland--dublin/music--performances/?page=1').text
soup = BeautifulSoup(html_text, 'lxml')

# search for all list elements matching this class in the soup and iterate over found items
events = soup.find_all('li', class_='search-main-content__events-list-item search-main-content__events-list-item__mobile')
for event in events:
    # scrape relevant info from their element attributes (found using inspect tool)
    name = event.find('h2', class_='Typography_root__4bejd #3a3247 Typography_body-lg__4bejd event-card__clamp-line--two Typography_align-match-parent__4bejd').text
    venue = event.find('p', class_='Typography_root__4bejd #585163 Typography_body-md__4bejd event-card__clamp-line--one Typography_align-match-parent__4bejd').text
    date = event.find('p', class_='Typography_root__4bejd #3a3247 Typography_body-md-bold__4bejd Typography_align-match-parent__4bejd').text
    link = event.find('div', class_='Stack_root__1ksk7').a.get('href') # store link to main page to grab price

    # make new request to event's main page and new soup
    event_html_text = requests.get(link).text
    event_page_soup = BeautifulSoup(event_html_text, 'lxml')

    # look for price, if it is not there display unavailable
    try:
        price = event_page_soup.find('div', class_='conversion-bar__panel-info').text
    except AttributeError:
        print(f'''
        Event Name  : {name}
        Event Venue : {venue}
        Event Date  : {date}
        Event Price : Unavailable''')
    else:
        print(f'''
        Event Name  : {name}
        Event Venue : {venue}
        Event Date  : {date}
        Event Price : {price}''')