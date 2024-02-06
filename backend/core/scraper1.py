import django
from django.conf import settings
from backend import backend_defaults

settings.configure(default_settings=backend_defaults, DEBUG=True)
django.setup()

# Now you can import your Django models
from backend.core.models import *

from playwright.sync_api import sync_playwright
# from pydantic_models import ResponseModel
# from models import *
from bs4 import BeautifulSoup
from rich import print
import requests
import json

EVENT_URL = "https://www.eventbrite.com/d/ireland--dublin/music--performances/"
EVENT_DATA_GET_URL = "https://www.eventbrite.com/api/v3/destination/events/?event_ids={}&page_size=20&expand=event_sales_status,image,primary_venue,ticket_availability,primary_organizer"
NEXT_BUTTON_SELECTOR = "button[data-spec='page-next']"


def navigate_to_page(context, url):
    """
    Navigate to a given URL using Playwright.
    """
    page = context.new_page()
    page.goto(url)
    return page


def extract_event_ids(soup):
    """
    Extract event IDs from a BeautifulSoup object.
    """
    event_ids_list = []
    script_tags = soup.find_all('script', type="application/ld+json")

    # TODO: continue JWR video "still the best way to scrape data." 24:35 / 41:00

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
    """
    Get event data from Eventbrite API.
    """
    event_ids_str = ",".join(map(str, event_ids))
    url = EVENT_DATA_GET_URL.format(event_ids_str)
    response = requests.get(url)
    data = json.loads(response.text)
    model_data = ResponseModel(**data)
    for event in model_data.events:
        print(event)
        # yield event


def run(p):
    """
    Run the Playwright scraper.
    """
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = navigate_to_page(context, EVENT_URL)
    
    # get list of events in html
    html = page.inner_html('body')
    soup = BeautifulSoup(html, 'html.parser')
    
    # click the next page button for as many pages of results there are
    while True:
        try:
            # create ResponseModel and send data to MongoDB server
            # then go to next page and repeat
            event_ids = extract_event_ids(soup)
            print(event_ids)
            event_data_get(event_ids)
            # for event in event_data_get(event_ids):
                # store_in_db(event.model_dump())
            break

            # uncomment when data is secure - don't spam requests
            # next_button = page.wait_for_selector(NEXT_BUTTON_SELECTOR)
            # if next_button:
            #     next_button.click()
            # else:
            #     break
        except Exception as e:
            print("Error occurred. Exiting.")
            print(e)
            break

    context.close()
    browser.close()


def main():
    with sync_playwright() as p:
        run(p)


if __name__ == "__main__":
    # import django
    # django.setup()
    main()