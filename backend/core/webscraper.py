# allow ability to run file as script in Django environment
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.spotevent.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import json
import random
import requests
from rich import print
from asyncio import sleep
from bs4 import BeautifulSoup
from backend.core.models import Event, Venue
from playwright.async_api import async_playwright


# constants
BASE_URL = "https://eventbrite.com/d/ireland--dublin/music--performances/" # URL for scraping
GET_EVENT_DATA_API_URL = "https://eventbrite.com/api/v3/destination/events/?event_ids={}&page_size=20&expand=event_sales_status,image,primary_venue,ticket_availability,primary_organizer" # URL for getting event data
NEXT_BUTTON_SELECTOR = "button[data-spec='page-next']" # selector for next button
FILE = 'backend/spotevent/data/event_ids/scraped_event_ids.txt' # file to write/read scraped event ids to/from
MAX_PAGES_TO_SCRAPE = 4 # max number of pages to scrape

async def navigate_to_page(context, url):
    """
    Navigate to a given URL using Playwright.
    """
    page = await context.new_page()
    await page.goto(url)

    await sleep(random.uniform(1, 3))

    return page


def write_event_ids_to_file(scraped_event_ids):
    """
    Write the scraped event IDs to a file.
    """
    with open(FILE, 'w') as f:
        for event_id in scraped_event_ids:
            f.write(f"{event_id}\n")


async def extract_event_ids(soup, start_index=0):
    """
    Extract event IDs from a BeautifulSoup object starting from a given index.
    """
    event_ids_list = []
    script_tags = soup.find_all('script', type="application/ld+json")

    # loop through all script tags
    for i in range(start_index, len(script_tags)):
        # get the script tag
        script = script_tags[i]

        # try to parse the JSON data
        try:
            # create JSON obj
            data = json.loads(script.get_text())
            # get url from json obj
            url = data.get('url')

            # if url exists and has a hyphen
            if url and '-' in url:
                # split url on hyphen and take last element AKA event ID
                event_id = url.rsplit('-', 1)[-1]
                # add event ID to list
                event_ids_list.append(event_id)
        # if json is invalid, skip
        except json.JSONDecodeError:
            continue

    return event_ids_list


async def get_scraped_event_ids():
    """
    Get the scraped event IDs and save to file
    """
    scraped_event_ids = []
    page_num = 1

    async with async_playwright() as playwright:
        # create a new browser context
        browser = await playwright.chromium.launch()
        context = await browser.new_context()

        # only run for 14 pages max
        while page_num <= MAX_PAGES_TO_SCRAPE:
            # update the URL to navigate to the next page
            url = f"{BASE_URL}?page={page_num}"
            print("on page :", page_num)

            # navigate to the page
            page = await navigate_to_page(context, url)
            
            # create a BeautifulSoup object from the page content
            soup = BeautifulSoup(await page.content(), 'html.parser')
            new_scraped_event_ids = await extract_event_ids(soup)

            # add the new event IDs to the list
            scraped_event_ids.extend(new_scraped_event_ids)
            print(f"page {page_num}'s event ids :", new_scraped_event_ids)

            # increment the page number
            page_num += 1
            print("loading next page...")

            # click the next button
            next_button = soup.select_one(NEXT_BUTTON_SELECTOR)

            # if there is no next button, break the loop
            if not next_button:
                break

        # add the scraped event IDs to the file
        with open('backend/spotevent/data/test-data/input-more.txt', 'w') as f:
            for event_id in scraped_event_ids:
                f.write(f"{event_id}\n")

        # close the page and browser context
        await context.close()
        await browser.close()

    return scraped_event_ids


async def create_event_venue(events):
    """
    Create new event and venue objects from the event data.
    """

    for count, event in enumerate(events):
        try:
            # create a new venue object
            new_venue = Venue.create_from_event(event)
            print(f"------------------------\nevent {count} / 20")
            print(new_venue)
            print("new venue id :", new_venue.venue_id)
        except Exception as e:
            print("Error occurred while creating venue object.")
            print(e)

        try:
            # create a new event object
            new_event = Event(event)
            new_event = Event.create_from_event_and_venue(event, new_venue)
            print(new_event)
            print("new event id :", new_event.event_id)
        except Exception as e:
            print("Error occurred while creating event object.")
            print(f"{e = }\n"
                  f"{event['name'] =}\n"
                  f"{event['eventbrite_event_id'] = }\n"
                  f"---------------------------"
                  )


async def get_event_data_from_API():
    """
    Get event data from the Eventbrite API.
    """

    # main loop to read ids from file and make API calls
    with open(FILE, 'r') as f:
        event_ids = f.read()
        event_ids = event_ids.split('\n')
        event_ids = [x.rstrip() for x in event_ids]
        venues = {}
        events = {}

        # for loop that creates new API call with 20 event IDs
        for i in range(0, len(event_ids), 20):
            # create a string of 20 event ids separated by commas
            event_ids_str = ','.join(event_ids[i:i+20])

            # create the API URL
            url = GET_EVENT_DATA_API_URL.format(event_ids_str)

            # make the API call
            response = requests.get(url)
            await asyncio.sleep(random.uniform(1, 3))

            try:
                data = json.loads(response.text)
                events = data['events']

                # call function to create new events and venues
                await create_event_venue(events)

            except json.decoder.JSONDecodeError:
                print("Error decoding JSON", response.text)
                return
            except KeyError:
                print("KeyError", response.text)
                return
            except Exception as e:
                print("Error occurred while making API call.", response.text)
                print(e)
    return (events, venues)


async def main():
    """
    Main function to run the scraper
    """
    scraped_event_ids = await get_scraped_event_ids()
    print("scraped_event_ids :", scraped_event_ids)
    print("Scraping IDs complete.")

    # write the scraped event IDs to a file
    write_event_ids_to_file(scraped_event_ids)
    print("Writing IDs to file complete.")

    await get_event_data_from_API()

    return


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())