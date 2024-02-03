import asyncio
from playwright.async_api import async_playwright
# from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pydantic_models import ResponseModel
import json

def event_data_get(page):
    # i want to select the <ul> tag with classname="search-main-content__events-list" and then select all <li> tags
    page.inner_html('')


async def run(p) -> None:
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://www.eventbrite.com/d/ireland--dublin/music--performances/")
    # event_details = "li div div+div section div section+section"
    # event_price_details = 'li > div > div.discover-search-desktop-card.discover-search-desktop-card--hiddeable > section > div > section.event-card-details > div > div > p'
    # await page.is_visible(event_price_details)
    
    # get list of events in html
    html = await page.inner_html('ul.search-main-content__events-list')
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.find_all('p'))
    
    # click the next page button for as many pages of results there are
    while True:
        try:
            events = soup.find_all('li')
            # print(events)

            # events = await page.query_selector_all('li div div+div section div section+section')
            for e in events:
                scraped_event = {}
                name = events.find_all('h2')
                print(name).text

                # event details
                # name = await e.query_selector('h2')
                # name = await e.query_selector('li > div > div.discover-search-desktop-card.discover-search-desktop-card--hiddeable > section > div > section.event-card-details > div > a > h2')
                # venue = await e.query_selector('p')
                # date = await e.query_selector('p')
                # link = await e.query_selector('div.Stack_root__1ksk7 a')

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