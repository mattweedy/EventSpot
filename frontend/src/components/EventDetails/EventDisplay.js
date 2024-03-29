import React, { useEffect, useState } from 'react';
import Modal from 'react-modal';
import EventVenueModalDisplay from './EventVenueModalDisplay';
import { FaTimes } from 'react-icons/fa';
import { toast } from 'react-hot-toast';
import axios from 'axios';

// TODO: pass username to here
// TODO: ensure recommended_events in User model is an array of event_ids

Modal.setAppElement('#root');

function EventDisplay({ event, venues, isRecommendation = false, username }) {
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [isSaved, setIsSaved] = useState(false);
    const toastOptions = {
        style: {
            borderRadius: '10px',
            background: '#333',
            color: '#fff',
            alignItems: 'center',
            justifyContent: 'center',
        },
        duration: 6000,
    };


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

    const handleSave = async (event_id) => {
        // send request to backend to save/remove the event
        try {
            let data = {
                username: username,
                event_id: event_id,
            };

            let isJson = true;

            // check if the data is JSON
            try {
                JSON.stringify(data);
            } catch (error) {
                isJson = false;
            }

            if (isJson) {
                // send the data
                const response = await axios.post('http://localhost:8000/api/save_remove_recommendation', data, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                // set the state based on the response and display a toast message
                setIsSaved(response.data.is_saved);
                toast.success(response.data.message, toastOptions);
            } else {
                console.error('The data is not JSON');
            }
        } catch (error) { // catch any errors
            console.error('Failed to save/remove recommendation:', error);
            toast.error('An error occurred while saving/removing the recommendation.', toastOptions);
        }
    }

    return (
        // <div className="event-display">
        <div className={`event-display ${isRecommendation ? 'recommendation' : ''}`}>
            <div className="eventDetails">
                <a href={event.tickets_url}><img src={event.image} className="event-image" alt=''></img></a>
                <h2 className="event-name">{event.name}</h2>
                <h4 className="event-venue-name"><span>{venue ? venue.name : 'Venue not found'}</span></h4>
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
                    console.log("showing venue modal", venue);
                    setModalIsOpen(true);
                }}>
                    Show Full Details
                </button>
                {isRecommendation && (
                    <button onClick={() => handleSave(event.event_id)} id={isSaved ? 'remove' : 'save'}>
                    {isSaved ? 'Remove Recommendation' : 'Save Recommendation'}
                </button>
                )}
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
                        height: 'fit-content',
                        maxHeight: '900px',
                        margin: 'auto',
                        borderRadius: '15px',
                    },
                }}
            >
                <button className="modal-close-button" onClick={() => setModalIsOpen(false)}><FaTimes /></button>
                <EventVenueModalDisplay event={event} venue={venue} />
            </Modal>
        </div>
    );
}

export default EventDisplay;