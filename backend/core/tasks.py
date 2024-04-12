from celery import shared_task
from . webscraper import *

# @shared_task
# def scrape_event_ids_task():
#     """
#     Scrape event IDs from the web and save to file.
#     """
#     # get the scraped event IDs
#     scraped_event_ids = get_scraped_event_ids()
#     # write the event IDs to a file
#     write_event_ids_to_file(scraped_event_ids)

# @shared_task
# def get_event_data_task():
#     """
#     Get event data from the web and save to file.
#     """
#     # get the event data and store in db
#     get_event_data_from_API()
