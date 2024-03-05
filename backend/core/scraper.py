import sys
print(sys.path)
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.spotevent.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from playwright.async_api import async_playwright
from backend.core.models import Event, Venue
from bs4 import BeautifulSoup
from rich import print
import requests
import json

EVENT_URL = "https://eventbrite.com/d/ireland--dublin/music--performances/"
EVENT_DATA_GET_URL = "https://eventbrite.com/api/v3/destination/events/?event_ids={}&page_size=20&expand=event_sales_status,image,primary_venue,ticket_availability,primary_organizer"
NEXT_BUTTON_SELECTOR = "button[data-spec='page-next']"

async def navigate_to_page(context, url):
    """
    Navigate to a given URL using Playwright.
    """
    page = await context.new_page()
    await page.goto(url)
    return page


async def extract_event_ids(soup, start_index):
    """
    Extract event IDs from a BeautifulSoup object starting from a given index.
    """
    event_ids_list = []
    script_tags = soup.find_all('script', type="application/ld+json")

    for i in range(start_index, len(script_tags)):
        script = script_tags[i]
        try:
            data = json.loads(script.get_text()) # create json obj
            url = data.get('url') # get url from json obj
            print(url)
            if url and '-' in url: # if url exists and has a hyphen
                event_id = url.rsplit('-', 1)[-1] # split url on hyphen and take last element AKA event ID
                event_ids_list.append(event_id) # add event ID to list
        except json.JSONDecodeError: # if json is invalid, skip
            continue

    return event_ids_list

# TODO: stop requesting API data
# TODO: get next button loop working
#       aka. get all event IDs from all pages
#       save all these to CSV or JSON or POSTGRES
#       then make requests for single ID
#       or 



# TODO: save to Postgres
# TODO: decide whether to do this in the scraper or in other backend file
async def event_data_get():
    """
    Get event data from Eventbrite API.
    """
    # script_dir = os.path.dirname(__file__)
    # file = os.path.join(script_dir, 'backend\\spotevent\\data/test-data/eventbrite-ids-04-03-24.txt')
    file = 'backend/spotevent/data/test-data/eventbrite-ids-04-03-24.txt'

    with open(file, 'r') as f:
        event_ids = f.read().rstrip().split('\n')
        venues = {}
        events = {}

        # for loop that creates new API call with 20 event IDs
        for i in range(0, len(event_ids), 20):
            # create a string of 20 event IDs separated by commas
            event_ids_string = ','.join(event_ids[i:i+20])
            # create API call URL with 20 event IDs
            url = EVENT_DATA_GET_URL.format(event_ids_string)
            # make API call
            response = requests.get(url)
            await asyncio.sleep(7)
    
            try:
                data = json.loads(response.text)
                events = data["events"]

                # for loop that creates new Venue and Event objects
                count = 0
                for event in events:
                    try:
                        new_venue = Venue.create_from_event(event)
                        print (f"------------------------\nevent {count}")
                        print(new_venue)
                        print("new venue id :", new_venue.venue_id)
                    except Exception as e:
                        print("Error occurred while creating venue object.")
                        print(e)

                    try:
                        new_event = Event(event)
                        new_event = Event.create_from_event_and_venue(event, new_venue)
                        print(new_event)
                        print("new event id :", new_event.event_id)
                    except Exception as e:
                        print("Error occurred while creating event object.")
                        print(e)
                    count += 1
            except json.decoder.JSONDecodeError:
                print("Error decoding JSON.", response.text)
                return
            except Exception as e:
                print("Error occurred while making API call.", response.text)
                print(e)
            
    return (events, venues)


async def run(p):
    """
    Run the Playwright scraper.
    """
    # browser = p.chromium.launch()
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await navigate_to_page(context, EVENT_URL)
    last_index = 0
    

    # click the next page button for as many pages of results there are
    while True:
        try:
            # get list of events from current page's html
            html = await page.inner_html('body')
            soup = BeautifulSoup(html, 'html.parser')

            # then go to next page and repeat
            event_ids = await extract_event_ids(soup, last_index)
            print(event_ids)

            last_index += len(event_ids)
            # uncomment when data is secure - don't spam requests
            next_button = await page.wait_for_selector(NEXT_BUTTON_SELECTOR)
            if next_button:
                await next_button.click()
            # TODO: getting Response 429 from Eventbrite API - TOO MANY REQUESTS

        except Exception as e:
            print("Error occurred. Exiting.")
            print(e)
            break

    await context.close()
    await browser.close()


async def main():
    """
    main function to run the scraper
    """
    await event_data_get()
    return

    # async with async_playwright() as p:
    #     await run(p)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())