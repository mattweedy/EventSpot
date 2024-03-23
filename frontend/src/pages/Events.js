import React, { useState, useEffect, } from 'react';
import { useLocation } from 'react-router-dom';
import SearchBar from '../components/General/SearchBar';
import useFetchData from '../components/Data/useFetchData';
import EventDisplay from '../components/EventDetails/EventDisplay';

// import DisplayEventVenueData from '../components/Data/DisplayEventVenueData';

const Events = () => {
    // TODO: change search bar to include venue name
    // ? maybe implement the edit preferences page first
    const [eventSearchTerm, setEventSearchTerm] = useState('');
    const [loadEvents, setLoadEvents] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
            setLoadEvents(true);
        }, 100); // adjust time

        return () => clearTimeout(timer);
    }, []);

    const events = useFetchData('/events/');
    const venues = useFetchData('/venues/');
    // const filteredEvents = events ? events.filter(event => event.name.toLowerCase().includes(eventSearchTerm.toLowerCase())) : null;
    const filteredEvents = events ? events.filter(event => {
        const eventVenue = venues ? venues.find(venue => venue.id === event.venue_id) : null;
        console.log("Event Venue:", eventVenue);
        const eventName = event.name.toLowerCase();
        const venueName = eventVenue ? eventVenue.name.toLowerCase() : '';
        return eventName.includes(eventSearchTerm.toLowerCase()) || venueName.includes(eventSearchTerm.toLowerCase());
    }) : null;
    const location = useLocation();

    useEffect(() => {
        const newHeight = location.pathname === '/events' ? '100vh' : '90vh';
        document.documentElement.style.setProperty('--dynamic-height', newHeight);
        console.log("Dynamic height set to:", newHeight);
    }, [location.pathname]);

    return (
        <div className="ev-con-con">
            {loadEvents && <SearchBar searchTerm={eventSearchTerm} setSearchTerm={setEventSearchTerm} />}
            <div className="events-container">
                {filteredEvents && filteredEvents.length === 0 ? <h4>Specified event not found.</h4> : null}
                {events && venues && filteredEvents.map(event => (
                    loadEvents ? (
                        <EventDisplay key={event.id} event={event} venues={venues} />
                    ) : (
                        <div className="skeleton-loader" id="events-skeleton"/>
                    )
                ))}
            </div>
        </div>
    );
};

export default Events;