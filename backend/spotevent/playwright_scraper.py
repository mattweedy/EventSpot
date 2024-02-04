from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pydantic_models import ResponseModel
import json

def event_data_get(soup):
    # select the json inside each script tag of type="application/ld+json" with beautiful soup passed from run() DO NOT USE BY CSS SELECTOR
    script_tags = soup.find_all('script', type="application/ld+json")

    print(script_tags.inner_html)

    # TODO: continue JWR video "still the best way to scrape data." 12:32 / 41:00
    # TODO: iterate over script tags, in the "url" key, get the event number from the event's url and return
    # TODO: from list of event IDs, generate api request to get event details
    # TODO: store event details in ResponseModel
    # TODO: store ResponseModel in database

    for script in script_tags:
        # load the json from the script tag
        event_info = json.loads(script.string)
        # check if the json contains the event key
        if "url" in event_info:
            # get the event number from the json
            eventbrite_event_id = 
            event_number = event_info["event"]["id"]
            print(event_number)
            return event_number
        else:
            print("No event found")
            return None


def run(p):
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.eventbrite.com/d/ireland--dublin/music--performances/")
    
    # get list of events in html
    html = page.inner_html('body')
    soup = BeautifulSoup(html, 'html.parser')
    
    # click the next page button for as many pages of results there are
    while True:
        try:
            data = event_data_get(soup)

            # uncomment when data is secure - don't spam requests
            # next_button = page.wait_for_selector("button[data-spec='page-next']", timeout=5000)
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


main()