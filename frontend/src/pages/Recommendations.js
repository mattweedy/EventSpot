import React, { useEffect, useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import axios from 'axios';
import EventDisplay from '../components/EventDetails/EventDisplay';
import useFetchData from '../components/Data/useFetchData';

function RecommendedEvents() {
    const { recommendedEventIds } = useOutletContext();

    
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

    return (
        <div>
            <h1>Recommended Events</h1>
            {recommendedEventIds === 0 ? (
                <h4>No recommended events found.</h4>
                ) : (
                    <div className="events-container">
                    {recommendedEvents ? (
                        recommendedEvents.map(event => (
                            <EventDisplay key={event.id} event={event} venues={venues}/>
                            ))
                            ) : (
                                <div className="skeleton-loader" id="events-skeleton" />
                                )}
                </div>
            )}
        </div>
    );
}

export default RecommendedEvents;