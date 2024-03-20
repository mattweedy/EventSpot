import React from 'react';

function VenueDisplay({ venue }) {
    console.log("VenueDisplay: venue", venue)
    return (
        <div className="venue-display">
            <h2 className="venue-name">{venue.name}</h2>
            <p className="venue-id">{venue.venue_id}</p>
            <p className="venue-address">{venue.address}</p>
            <p className="venue-summary">{venue.summary}</p>
        </div>
    );
}

export default VenueDisplay;