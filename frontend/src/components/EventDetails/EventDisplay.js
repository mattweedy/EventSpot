import React, { useState } from 'react';
import Modal from 'react-modal';
// import VenueDisplay from './VenueDisplay';

Modal.setAppElement('#root');

function EventDisplay({ event, venues }) {
    // const [showVenue, setShowVenue] = useState(false);
    const [modalIsOpen, setModalIsOpen] = useState(false);

    if (!event) {
        return null;
    }

    const venue = venues ? venues.find(venue => venue.id === event.venue_id) : null;

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
            <hr></hr>
            <div>
                <button className="expandDetails" onClick={() => { //setShowVenue(!showVenue);
                    console.log("showing venue", venue);
                    setModalIsOpen(true);
                    }}>
                    {/* {showVenue ? 'Hide Details' : 'Show Full Details'} */}
                    Show Full Details
                </button>
            </div>
            <Modal
                isOpen={modalIsOpen}
                onRequestClose={() => setModalIsOpen(false)}
                contentLabel="Event Details"
                style={{
                    overlay: {
                        backgroundColor: 'rgba(0, 0, 0, 0.75)',
                        zIndex: '1000',
                        backdropFilter: 'blur(3px)',
                    },
                    content: {
                        color: 'lightsteelblue',
                    },
                }}
            >
                {/* <h2>{event.name}</h2>
                <p>{event.summary}</p>
                <p>€{event.price}</p>
                <p>{event.date}</p> */}
                
                {/* {venue && <VenueDisplay venue={venue} />} */}
                <button onClick={() => setModalIsOpen(false)}>Close</button>
            </Modal>
        </div>
    );
}

export default EventDisplay;