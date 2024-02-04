import asyncio
from playwright.async_api import async_playwright
# from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pydantic_models import ResponseModel
import json

async def event_data_get(soup):
    # select the json inside each script tag of type="application/ld+json" with beautiful soup passed from run() DO NOT USE BY CSS SELECTOR
    script_tags = soup.find_all('script', type="application/ld+json")
    for script in script_tags:
        # load the json from the script tag
        event_info = json.loads(script.string)
        # check if the json contains the event key
        if "event" in event_info:
            # get the event number from the json
            event_number = event_info["event"]["id"]
            print(event_number)
            return event_number
        else:
            print("No event found")
            return None


async def run(p) -> None:
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://www.eventbrite.com/d/ireland--dublin/music--performances/")
    
    # get list of events in html
    html = await page.inner_html('body')
    soup = BeautifulSoup(html, 'html.parser')
    
    # click the next page button for as many pages of results there are
    while True:
        try:
            data = await event_data_get(soup)


            next_button = await page.wait_for_selector("button[data-spec='page-next']")
            await next_button.click()
        except:
            break

    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as p:
        await run(p)


asyncio.run(main())