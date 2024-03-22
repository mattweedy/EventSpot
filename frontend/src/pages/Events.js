import React from 'react';

const Events = () => {
    const event = {
        title: 'Example Event',
        date: '2022-12-31',
        location: 'New York City',
        description: 'This is an example event description.'
    };

    return (
        <div>
            <h1>Events Page</h1>
            <div>
                <h2>{event.title}</h2>
                <p>Date: {event.date}</p>
                <p>Location: {event.location}</p>
                <p>Description: {event.description}</p>
            </div>
        </div>
    );
};

export default Events;