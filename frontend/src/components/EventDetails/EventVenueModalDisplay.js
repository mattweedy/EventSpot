import React, { useState, useEffect } from 'react';

export default function EventVenueModelDisplay({ event, venue }) {
    const apiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;
    const [loadMap, setLoadMap] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
            setLoadMap(true);
        }, 1000); // adjust time

        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="modal-display">
            <div className="modal-top">
                <div id="modal-event">
                    <div id="modal-image">
                        <a href={event.tickets_url}><img src={event.image} alt={event.name} /></a>
                    </div>
                    <div id="modal-event-details">
                        <h2>{event.name}</h2>
                        <p><span>Description: </span>{event.summary}</p>
                    </div>
                </div>
                {venue.city && (
                    <div id="modal-venue">
                        <div id="modal-venue-map">
                            {loadMap ? (
                                <iframe
                                    title="venue-map"
                                    width="100%"
                                    height="400px"
                                    style={{border:0, borderRadius: '15px'}}
                                    loading="lazy"
                                    allowFullScreen
                                    src={`https://www.google.com/maps/embed/v1/place?key=${apiKey}&q=${encodeURIComponent(venue.address + (venue.city ? ', ' + venue.city : ''))}`}>
                                </iframe>
                            ) : (
                                <div className="skeleton-loader" />
                            )}
                        </div>
                        <div id="modal-venue-details">
                            <h2>{venue.name}</h2>
                            <p><span>Location: </span>{venue.address}</p>
                            <p><span>City: </span>{venue.city}</p>
                        </div>
                    </div>
                )}
            </div>
            <div id="modal-buy-tickets-button-container">
                <p className="event-price"><span>€{event.price}</span></p>
                <p className="event-date">
                    {new Date(event.date).toLocaleDateString('en-IE', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                    })}
                </p>
                <a href={event.tickets_url} ><button id="modal-buy-tickets-button">Get Tickets</button></a>
            </div>
        </div>
    );
}