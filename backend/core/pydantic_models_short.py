from typing import Optional
from pydantic import BaseModel
from datetime import date, time


class VenueModel(BaseModel):
    id: int
    name: str
    venue_id: str
    address: str
    city: str
    country: str


class EventModel(BaseModel):
    id: int
    name: str
    event_id: str
    price: float
    venue: VenueModel
    image: str
    tags: str
    tickets_url: str
    date: date
    start_time: time
    end_time: time
    summary: Optional[str]
    status: str

# responsemodel contains one event and its venue
class ResponseModel(BaseModel):
    events: list[EventModel]
    venues: list[VenueModel]
    def __init__(self, events, **kwargs):
        events = events["events"]