import React, { useEffect, useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import SearchBar from '../components/General/SearchBar';
import useFetchData from '../components/Data/useFetchData';
import EventDisplay from '../components/EventDetails/EventDisplay';
import { useDynamicHeight } from '../components/General/useDynamicHeight';

export default function Recommendation() {
    const { setRecommendedEventIds } = useOutletContext();
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
        // get the events from local storage
        const storedEvents = localStorage.getItem('recommendedEvents');
        if (storedEvents) {
            const parsedEvents = JSON.parse(storedEvents);
            setRecommendedEvents(parsedEvents);

            // extract event_ids from each event and set recommendedEventIds
            const eventIds = parsedEvents.map(event => event.event_id);
            setRecommendedEventIds(eventIds);
        }
        // eslint-disable-next-line
    }, []);

    
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