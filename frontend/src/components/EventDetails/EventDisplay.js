import React, { useState } from 'react';
import VenueDisplay from './VenueDisplay';

function EventDisplay({ event, venues }) {
    const [showVenue, setShowVenue] = useState(false);

    if (!event) {
        return null;
    }

    const venue = venues ? venues.find(venue => venue.venue_id === event.venue_id) : null;

    return (
        <div className="event-display">
            <a href={event.tickets_url}><img src={event.image} className="event-image" alt=''></img></a>
            <h2 className="event-name">{event.name}</h2>
            {/* TODO: REMOVE ID - DEBUG  */}
            <p className="event-id">{event.event_id}</p>
            <p className="event-summary">{event.summary}</p>
            <p className="event-price">€{event.price}</p>
            <p className="event-date">{event.date}</p>
            <a href={event.tickets_url} className="event-ticket-link">buy tickets</a>
            <div>
                <button onClick={() => setShowVenue(!showVenue)}>
                    {showVenue ? 'Hide Venue Details' : 'Show Venue Details'}
                </button>
            </div>
            {showVenue && venue && <VenueDisplay venue={venue} />}
        </div>
    );
}

export default EventDisplay;