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
                const events = response.data;
                const filteredEvents = [];
                const recommendedEventIdsAsNumbers = Object.keys(recommendedEventIds).map(Number);

                for (let i = 0; i < recommendedEventIdsAsNumbers.length && filteredEvents.length < 10; i++) {
                    const event = events.find(e => e.id === recommendedEventIdsAsNumbers[i]);
                    if (event) {
                        filteredEvents.push(event);
                    }
                }

                console.log("filtered events : ", filteredEvents);
                setRecommendedEvents(filteredEvents);
            } catch (error) {
                console.error('Failed to fetch events:', error);
            }
        };

        fetchEvents();
    }, [recommendedEventIds]);

    console.log("rec events : ", recommendedEvents);

    return (
        <div>
            {recommendedEvents.map(event => (
                <EventDisplay key={event.id} event={event} venues={venues}/>
            ))}
        </div>
    );
}

export default RecommendedEvents;