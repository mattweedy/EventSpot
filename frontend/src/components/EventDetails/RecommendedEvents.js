import React, { useEffect, useState } from 'react';
import axios from 'axios';
import EventDisplay from './EventDisplay';
import useFetchData from '../Data/useFetchData';

function RecommendedEvents({ recommendedEventIds }) {
    const [recommendedEvents, setRecommendedEvents] = useState([]);
    const venueData = useFetchData('/venues/');
    const [venues, setVenues] = useState([]);

    useEffect(() => {
        setVenues(venueData);
    }, [venueData]);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/events');
                const allEvents = response.data;

                let events = allEvents.filter(e => recommendedEventIds.includes(e.event_id));

                // Sort events based on the order of recommendedEventIds
                events.sort((a, b) => recommendedEventIds.indexOf(a.event_id) - recommendedEventIds.indexOf(b.event_id));

                console.log("Recommended Event Ids: ", recommendedEventIds); // print recommended event ids
                setRecommendedEvents(events);
            } catch (error) {
                console.error('Failed to fetch events:', error);
            }
        };

        fetchEvents();
    }, [recommendedEventIds]);

    console.log("rec events : ", recommendedEvents);

    return (
        <div className="events-container">
            {recommendedEvents.map(event => (
                <EventDisplay key={event.id} event={event} venues={venues}/>
            ))}
        </div>
    );
}

export default RecommendedEvents;