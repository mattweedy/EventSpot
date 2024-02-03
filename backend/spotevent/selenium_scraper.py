from selenium import webdriver
from selenium.webdriver.common.by import By
from pydantic_models import ResponseModel
import json

def event_data_get(driver, eventId:str):
    driver.get(f"https://www.eventbrite.com/e/{eventId}.html")
    script_tag = driver.find_element_by_tag_name(By.CSS_SELECTOR, "div#listings-root+script")
    event_info = json.loads(script_tag.get_attribute("innerHTML")).replace("window.__SERVER_DATA__ = ", "")
    event_number = event_info["event"]["id"]
    return event_number

def review_data_get():
    pass


def main():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    events = [""]

    for event in events:
        event_number = event_data_get(driver, event)
        print(event_number)


if __name__ == "__main__":
    main()