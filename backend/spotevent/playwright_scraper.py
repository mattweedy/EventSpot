from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pydantic_models import ResponseModel
import json
import asyncio

def event_data_get(page):
    # i want to select the <ul> tag with classname="search-main-content__events-list" and then select all <li> tags
    page.inner_html('')


async def run(p) -> None:
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://www.eventbrite.com/d/ireland--dublin/music--performances/")
    
    # click the next page button for as many pages of results there are
    while True:
        try:
            next_button = page.wait_for_selector("button[data-spec='page-next']")
            next_button.click()
        except:
            break

    await context.close()
    await browser.close()


async def main() -> None:
    async with sync_playwright() as p:
        await run(p)


asyncio.run(main())