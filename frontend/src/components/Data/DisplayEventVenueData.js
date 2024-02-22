import React, { useState } from 'react';
import useFetchData from './useFetchData';

const DisplayEventVenueData = () => {
    const [isDataVisible, setIsDataVisible] = useState(false);
    const events = useFetchData('/events/');
    const venues = useFetchData('/venues/');

    return (
        <div>
            <button onClick={() => setIsDataVisible(!isDataVisible)}>
                {isDataVisible ? 'Hide Events and Venues' : 'Show Events and Venues'}
            </button>

            {isDataVisible && (
                <div style={{ display: 'flex' }}>
                    <div style={{ flex: 1 }}>
                    <h1>Events</h1>
                        <hr></hr>
                        {events && events.map(event => (
                            <div key={event.id}>
                                <img src={event.image} style={{ maxWidth: "50%" }} alt=''></img>
                                <h2>{event.name}</h2>
                                <p>{event.event_id}</p>
                                <p>{event.price}</p>
                                <p>{event.summary}</p>
                                <a href={event.tickets_url}>tickets</a>
                            </div>
                        ))}
                    </div>

                    <div style={{ flex: 1 }}>
                    <h1>Venues</h1>
                        <hr></hr>
                        {venues && venues.map(venue => (
                            <div key={venue.id}>
                                <h2>{venue.name}</h2>
                                <p>{venue.venue_id}</p>
                                <p>{venue.address}</p>
                                <p>{venue.summary}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* <h1 style={{ textAlign: 'center' }}>Event Data Generated From Django</h1>
            <div style={{ display: 'flex' }}>
                <div style={{ flex: 1 }}>
                    {events && events.map(event => (
                        <div key={event.id}>
                            <hr></hr>
                            <img src={event.image} style={{ maxWidth: "50%" }} alt=''></img>
                            <h2>{event.name}</h2>
                            <p>{event.event_id}</p>
                            <p>{event.price}</p>
                            <p>{event.summary}</p>
                            <a href={event.tickets_url}>tickets</a>
                        </div>
                    ))}
                </div>
                <div style={{ flex: 1 }}>
                    {venues && venues.map(venue => (
                        <div key={venue.id}>
                            <hr></hr>
                            <h2>{venue.name}</h2>
                            <p>{venue.venue_id}</p>
                            <p>{venue.address}</p>
                            <p>{venue.summary}</p>
                        </div>
                    ))}
                </div>
            </div> */}
        </div>
    );
};

export default DisplayEventVenueData;