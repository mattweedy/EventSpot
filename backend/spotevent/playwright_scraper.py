from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# close browser when finished
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.eventbrite.com/d/ireland--dublin/music--performances/")
    page.inner_html()