from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Pagination(BaseModel):
    object_count: int
    continuation: Any
    page_count: int
    page_size: int
    has_more_items: bool
    page_number: int


class Image(BaseModel):
    url: str
    id: str


class Collection(BaseModel):
    status: str
    _type: str
    name: str
    relative_url: str
    is_autocreated: bool
    absolute_url: str
    summary: str
    organization_id: str
    image_id: str
    id: str
    organizer_id: str
    event_ids: List[str]
    type: str
    slug: str
    is_private: bool


class MaximumTicketPrice(BaseModel):
    currency: str
    major_value: str
    value: int
    display: str


class MinimumTicketPrice(BaseModel):
    currency: str
    major_value: str
    value: int
    display: str


class TicketAvailability(BaseModel):
    maximum_ticket_price: MaximumTicketPrice
    minimum_ticket_price: MinimumTicketPrice
    is_free: bool
    has_bogo_tickets: bool
    has_available_tickets: bool
    is_sold_out: bool


class Tag(BaseModel):
    prefix: str
    tag: str
    display_name: str
    _type: Optional[str] = None


class Address(BaseModel):
    city: str
    country: str
    region: str
    longitude: str
    localized_address_display: str
    postal_code: Optional[str] = None
    address_1: str
    address_2: str
    latitude: str
    localized_multi_line_address_display: List[str]
    localized_area_display: str


class PrimaryVenue(BaseModel):
    _type: str
    name: str
    venue_profile_id: Any
    address: Address
    venue_profile_url: str
    id: str


class PrimaryOrganizer(BaseModel):
    _type: str
    num_upcoming_events: Any
    name: str
    profile_type: str
    num_followers: int
    url: str
    twitter: Optional[str]
    summary: Optional[str]
    num_saves: Any
    image_id: Optional[str]
    followed_by_you: bool
    facebook: Optional[str]
    num_collections: Any
    id: str
    website_url: Optional[str]
    num_following: Any


class Event(BaseModel):
    id: str
    name: str
    url: str
    primary_venue: PrimaryVenue
    primary_venue_id: str
    primary_organizer: PrimaryOrganizer
    eventbrite_event_id: str
    summary: Optional[str]
    tags: List[Tag]
    image: Image
    image_id: str
    timezone: str
    tickets_url: str
    start_date: str
    end_date: str
    start_time: str
    end_time: str
    status: str
    _type: str
    ticket_availability: TicketAvailability
    is_cancelled: Any
    hide_start_date: bool


class ResponseModel(BaseModel):
    pagination: Pagination
    events: List[Event]
