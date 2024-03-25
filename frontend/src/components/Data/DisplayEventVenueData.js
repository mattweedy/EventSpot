import React from 'react';
import EventDisplay from '../EventDetails/EventDisplay';

// ! Delete this file along with App2.js, Sidebar2.js

const DisplayEventVenueData = ({ events, venues }) => {
    return (
        <div className="ev-con-con">
                <div className="events-container">
                    {events && venues && events.map(event => (
                        <EventDisplay key={event.id} event={event} venues={venues} />
                    ))}
                </div>
        </div>
    );
};

export default DisplayEventVenueData;