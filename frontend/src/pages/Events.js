import React, { useState, useEffect, } from 'react';
import SearchBar from '../components/General/SearchBar';
import useFetchData from '../components/Data/useFetchData';
import EventDisplay from '../components/EventDetails/EventDisplay';
import { useDynamicHeight } from '../components/General/useDynamicHeight';


const Events = () => {
    const [eventSearchTerm, setEventSearchTerm] = useState('');
    const [loadEvents, setLoadEvents] = useState(false);

    useDynamicHeight();

    useEffect(() => {
        const timer = setTimeout(() => {
            setLoadEvents(true);
        }, 100); // adjust time

        return () => clearTimeout(timer);
    }, []);

    const events = useFetchData('/events/');
    const venues = useFetchData('/venues/');
    const filteredEvents = events ? events.filter(event => {
        const eventVenue = venues ? venues.find(venue => venue.id === event.venue_id) : null;
        const eventName = event.name.toLowerCase();
        const venueName = eventVenue ? eventVenue.name.toLowerCase() : '';
        return eventName.includes(eventSearchTerm.toLowerCase()) || venueName.includes(eventSearchTerm.toLowerCase());
    }) : null;

    return (
        <div className="ev-con-con">
            <h1>Browse and Search All Events</h1>
            {loadEvents && <SearchBar searchTerm={eventSearchTerm} setSearchTerm={setEventSearchTerm} />}
            <div className="events-container">
                {filteredEvents && filteredEvents.length === 0 ? <h4>Specified event not found.</h4> : null}
                {events && venues && filteredEvents.map(event => (
                    loadEvents ? (
                        <EventDisplay key={event.id} event={event} venues={venues} />
                    ) : (
                        <div className="skeleton-loader" id="events-skeleton" />
                    )
                ))}
            </div>
        </div>
    );
};

export default Events;