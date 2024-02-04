from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pydantic_models import ResponseModel
import requests
import json

EVENT_URL = "https://www.eventbrite.com/d/ireland--dublin/music--performances/"
EVENT_DATA_GET_URL = "https://www.eventbrite.com/api/v3/destination/events/?event_ids={}&page_size=20&expand=event_sales_status,image,primary_venue,ticket_availability,primary_organizer"
NEXT_BUTTON_SELECTOR = "button[data-spec='page-next']"

def navigate_to_page(p, url):
    """
    Navigate to a given URL using Playwright.

    Parameters:
    p (playwright.sync_api._generated.SyncPlaywright): The Playwright object.
    url (str): The URL to navigate to.

    Returns:
    playwright.sync_api._generated.Page: The Page object for the navigated page.
    """
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    return page

def extract_event_ids(soup):
    """
    Extract event IDs from a BeautifulSoup object.

    Parameters:
    soup (bs4.BeautifulSoup): The BeautifulSoup object to extract event IDs from.

    Returns:
    list of str: The extracted event IDs.
    """
    event_ids_list = []
    script_tags = soup.find_all('script', type="application/ld+json")

    # TODO: continue JWR video "still the best way to scrape data." 24:35 / 41:00
    # TODO: store event details in ResponseModel
    # TODO: store ResponseModel in mongoDB database

    for script in script_tags:
        try:
            data = json.loads(script.get_text()) # create json obj
            url = data.get('url') # get url from json obj
            if url and '-' in url: # if url exists and has a hyphen
                event_id = url.rsplit('-', 1)[-1] # split url on hyphen and take last element AKA event ID
                event_ids_list.append(event_id) # add event ID to list
        except json.JSONDecodeError: # if json is invalid, skip
            continue

    return event_ids_list


def event_data_get(event_ids):
    event_ids_str = ",".join(map(str, event_ids))
    # url = f"https://www.eventbrite.com/api/v3/destination/events/?event_ids={event_ids_str}&page_size=20&expand=event_sales_status,image,primary_venue,ticket_availability,primary_organizer"
    url = EVENT_DATA_GET_URL.format(event_ids_str)
    response = requests.get(url)
    print(response.json())



def run(p):
    page = navigate_to_page(p, EVENT_URL)
    
    # get list of events in html
    html = page.inner_html('body')
    soup = BeautifulSoup(html, 'html.parser')
    
    # click the next page button for as many pages of results there are
    while True:
        try:
            # successfully printing 20 event IDs from page
            # next generate url to grab their details
            # create json file and send data to MongoDB server
            # then go to next page and repeat
            event_ids = extract_event_ids(soup)
            print(event_ids)
            event_data_get(event_ids)
            break

            # uncomment when data is secure - don't spam requests
            # next_button = page.wait_for_selector(NEXT_BUTTON_SELECTOR)
            # if next_button:
            #     next_button.click()
            # else:
            #     break
        except:
            break

    context.close()
    browser.close()


def main():
    with sync_playwright() as p:
        run(p)


if __name__ == "__main__":
    main()