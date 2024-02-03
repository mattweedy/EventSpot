from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def event_data_get(page, eventId:str):
    page.goto(f"https://www.eventbrite.com/e/{eventId}.html")
    html_content = page.content()
    soup = BeautifulSoup(html_content, "html.parser")
    ul_tag = soup.find('ul', class_='search-main-content__events-list')
    li_tags = ul_tag.find_all('li') if ul_tag else []
    return li_tags

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.eventbrite.com/d/ireland--dublin/music--performances/")

        events = [""]

        for event in events:
            li_tags = event_data_get(page, event)
            for li in li_tags:
                print(li)

        browser.close()

if __name__ == "__main__":
    main()