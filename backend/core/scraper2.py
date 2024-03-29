from asyncio import sleep
import sys
print(sys.path)
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.spotevent')
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

# base_url = "https://eventbrite.com/d/ireland--dublin/music--performances/"
base_url = "https://www.eventbrite.com/d/ireland--dublin/music--performances--this-month/"


# Number of pages to scrape


async def test():
    url = base_url
    page_num = 1
    all_event_ids = []

    while True:
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            

            # Check if the page exists
            if response.status_code == 404:
                print("reached a page that doesn't exist...")
                break
            elif response.status_code == 429:
                print("too many requests...")
                break

            print(response.text)
            # Parse the response with BeautifulSoup
            print("on page :", page_num)
            # soup = BeautifulSoup(response.text, 'html.parser')
            # Extract event ids and add them to the list
            all_event_ids.extend(await extract_event_ids(event_page_soup))
            # Increment the page number and update the URL for the next iteration
            page_num += 1
            url = f"{base_url}?page={page_num}"
            print("current event ids :", all_event_ids)
            sleep(1000)
            print("loading next page...")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

    # Print all scraped event ids
    print(all_event_ids)

async def navigate_to_page(context, url):
    """
    Navigate to a given URL using Playwright.
    """
    page = await context.new_page()
    await page.goto(url)
    return page


async def extract_event_ids(soup, start_index=0):
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
            # print(url)
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

async def get_all_event_ids():
    event_ids = []
    page_num = 1
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        while page_num <= 10:
            # Update the URL to navigate to the next page
            url = f"{EVENT_URL}?page={page_num}"
            print("on page :", page_num)
            page = await navigate_to_page(context, url)
            soup = BeautifulSoup(await page.content(), 'html.parser')
            new_event_ids = await extract_event_ids(soup)
            event_ids.extend(new_event_ids)
            print(f"page {page_num}'s event ids :", new_event_ids)
            page_num += 1
            print("loading next page...")
            next_button = soup.select_one(NEXT_BUTTON_SELECTOR)
            if not next_button:
                break
        await context.close()
    return event_ids


# TODO: decide whether to do this in the scraper or in other backend file
async def event_data_get(event_ids):
    """
    Get event data from Eventbrite API.
    """
    event_ids_str = ",".join(map(str, event_ids))
    print(len(event_ids))
    url = EVENT_DATA_GET_URL.format(event_ids_str)
    response = requests.get(url)
    # TODO: DEBUGGING
    # 429 error back
    print("response.text : ",response.text)
    try:
        data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON.")
        return
    venues = {}
    events = {}

    for event, num in enumerate(data["events"]):
        new_venue = Venue(event)
        new_venue.to_csv(f'backend/spotevent/data/events-csv/venue{num}.csv')
        # if new_venue.venue_id not in venues:
        if new_venue.name not in venues:
            # venues[new_venue.venue_id] = new_venue
            venues[new_venue.name] = new_venue
            # print(new_venue.venue_id)
            print(new_venue.name)
            new_venue.save()
    
        new_event = Event(event)
        new_event.to_csv(f'backend/spotevent/data/events-csv/event{num}.csv')
        # if new_event.event_id not in events:
        if new_event.name not in events:
            # events[new_event.event_id] = new_event
            events[new_event.name] = new_event
            # print(new_event.event_id)
            print(new_event.name)
            new_event.save()

    return (events, venues)


async def run(p):
    """
    Run the Playwright scraper.
    """
    # browser = p.chromium.launch()
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await navigate_to_page(context, EVENT_URL)
    

    # click the next page button for as many pages of results there are
    while True:
        try:
            # get list of events from current page's html
            html = await page.inner_html('body')
            soup = BeautifulSoup(html, 'html.parser')

            # then go to next page and repeat
            event_ids = await extract_event_ids(soup)
            print(event_ids)
            # uncomment when data is secure - don't spam requests
            next_button = await page.wait_for_selector(NEXT_BUTTON_SELECTOR)
            if next_button:
                await next_button.click()
                # await page.wait_for_timeout(20000)

            # try:
            #     events, venues = await event_data_get(event_ids)
            # except TypeError:
            #     print("Error occurred while getting event and venue data.")
            #     await context.close()
            #     await browser.close()
            #     break
            # print(events)
            # print(venues)
            # break
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
    event_ids = await get_all_event_ids()
    print(event_ids)

    # write event_ids to file
    with open('backend/spotevent/data/test-data/input-more.txt', 'w') as f:
        for event_id in event_ids:
            f.write(f"{event_id}\n")
    return

    async with async_playwright() as p:
        await run(p)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())