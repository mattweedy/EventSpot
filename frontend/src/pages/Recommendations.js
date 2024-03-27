import React, { useEffect, useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import axios from 'axios';
import SearchBar from '../components/General/SearchBar';
import useFetchData from '../components/Data/useFetchData';
import EventDisplay from '../components/EventDetails/EventDisplay';
import { useDynamicHeight } from '../components/General/useDynamicHeight';

export default function Recommendation() {
    const { recommendedEventIds } = useOutletContext();
    const [recommendedEvents, setRecommendedEvents] = useState([]);
    const [venues, setVenues] = useState([]);
    const venueData = useFetchData('/venues/');
    const [eventSearchTerm, setEventSearchTerm] = useState('');
    const { userProfile } = useOutletContext();
    
    useDynamicHeight();

    useEffect(() => {
        setVenues(venueData);
    }, [venueData]);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/events');
                const allEvents = response.data;
                let events;

                try {
                    events = allEvents.filter(e => recommendedEventIds.includes(e.event_id));
                } catch (error) {
                    console.error('Failed to filter events:', error);
                }

                // sort events based on the order of recommendedEventIds
                events.sort((a, b) => recommendedEventIds.indexOf(a.event_id) - recommendedEventIds.indexOf(b.event_id));
                console.log("Recommended Event Ids: ", recommendedEventIds);

                setRecommendedEvents(events);
            } catch (error) {
                console.error('Failed to fetch events:', error);
            }
        };

        fetchEvents();
    }, [recommendedEventIds]);

    const filteredEvents = recommendedEvents ? recommendedEvents.filter(event => {
        const eventVenue = venues ? venues.find(venue => venue.id === event.venue_id) : null;
        const eventName = event.name.toLowerCase();
        const venueName = eventVenue ? eventVenue.name.toLowerCase() : '';
        return eventName.includes(eventSearchTerm.toLowerCase()) || venueName.includes(eventSearchTerm.toLowerCase());
    }) : null;

    return (
        <div className="ev-con-con">
            <h1>Recommended Events</h1>
            {recommendedEvents && recommendedEvents.length > 0 && <SearchBar searchTerm={eventSearchTerm} setSearchTerm={setEventSearchTerm} />}
            {recommendedEvents && recommendedEvents.length === 0 && <h2>No recommended events.</h2>}
            <div className="events-container">
                {recommendedEvents && recommendedEvents.length > 0 && filteredEvents && filteredEvents.length === 0 ? <h4>No events found for this search.</h4> : null}
                {recommendedEvents && venues ? (
                    filteredEvents.map(event => (
                        <EventDisplay key={event.id} event={event} venues={venues} isRecommendation={true} username={userProfile.display_name}/>
                    ))
                ) : (
                    <div className="skeleton-loader" id="events-skeleton" />
                )}
            </div>
        </div>
    );
}