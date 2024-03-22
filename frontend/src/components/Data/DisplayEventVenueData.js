import React from 'react';
import useFetchData from './useFetchData';
import EventDisplay from '../EventDetails/EventDisplay';

const DisplayEventVenueData = ({ isEventsVisible}) => {
    const events = useFetchData('/events/');
    const venues = useFetchData('/venues/');

    return (
        <div className="ev-con-con">
            {isEventsVisible && (
                <div className="events-container">
                    {events && events.map(event => (
                        <EventDisplay key={event.id} event={event} venues={venues} />
                    ))}
                </div>
            )}
        </div>
    );
};

export default DisplayEventVenueData;