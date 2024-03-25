import React, { useEffect, useState } from 'react';
import Modal from 'react-modal';
import EventVenueModelDisplay from './EventVenueModalDisplay';
import { FaTimes } from 'react-icons/fa';

Modal.setAppElement('#root');

function EventDisplay({ event, venues }) {
    const [modalIsOpen, setModalIsOpen] = useState(false);
    

    // prevent background scrolling when modal is open
    useEffect(() => {
        if (modalIsOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'auto';
        }

        // cleanup function
        return () => {
            document.body.style.overflow = 'auto';
        };
    }, [modalIsOpen]);

    // if there is no event, return null
    if (!event) {
        return null;
    }

    // find the venue for the event or set it to null
    const venue = venues ? venues.find(venue => venue.id === event.venue_id) : null;

    return (
        <div className="event-display">
            <div className="eventDetails">
            <a href={event.tickets_url}><img src={event.image} className="event-image" alt=''></img></a>
            <h2 className="event-name">{event.name}</h2>
            <h4 className="event-venue-name"><span>{venue.name}</span></h4>
            <p className="event-id">{event.event_id}</p>
            <p className="event-date">
                {new Date(event.date).toLocaleDateString('en-IE', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                })}    
            </p>
            <p className="event-summary">{event.summary}</p>
            </div>
            <div className="showFullDetails">
                <p className="event-price">€{event.price}</p>
                <a href={event.tickets_url} className="event-ticket-link"><button>Get Tickets</button></a>
                <button className="expandDetails" onClick={() => {
                    console.log("showing venue", venue);
                    setModalIsOpen(true);
                    }}>
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
                        backdropFilter: 'blur(2px)',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                    },
                    content: {
                        color: '#fff',
                        backgroundColor: '#202020',
                        border: 'none',
                        width: '85%',
                        maxWidth: '1050px',
                        // height: '85%',
                        height: 'fit-content',
                        maxHeight: '900px',
                        margin: 'auto',
                        borderRadius: '15px',
                    },
                }}
            >
                <button className="modal-close-button" onClick={() => setModalIsOpen(false)}><FaTimes /></button>
                <EventVenueModelDisplay event={event} venue={venue} />
            </Modal>
        </div>
    );
}

export default EventDisplay;