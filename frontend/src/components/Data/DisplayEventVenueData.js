import React, { useState } from 'react';
import useFetchData from './useFetchData'; // Assuming you have this custom hook
import EventDisplay from '../EventDetails/EventDisplay'; // Import the EventDisplay component

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