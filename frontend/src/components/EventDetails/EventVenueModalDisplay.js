export default function EventVenueModelDisplay({ event, venue }) {
    // TODO: design ((fullscreen)) dtisplay for both event and venue details
    // maybe big image from top left corner to middle of screen
    // then event details on left side of screen
    // and venue details on right side of screen
    // with a close button at the bottom/top right corner
    // and a button to buy tickets at the bottom right corner
    // TODO: in modal-venue-map, display a map of the venue using the venue.address
    // TODO: setup google maps api key

    return (
        <div className="modal-display">
            <div id="modal-event">
                <div id="modal-image">
                <a href={event.tickets_url}><img src={event.image}/></a>
                </div>
                <div id="modal-event-details">
                    <h2>{event.name}</h2>
                    <p>{event.summary}</p>
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
            <div id="modal-venue">
                <div id="modal-venue-details">
                    <h2>{venue.name}</h2>
                    <p>{venue.address}</p>
                    <p>{venue.city}</p>
                </div>
                <div>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    space for map
                </div>
                {/* <div id="modal-venue-map">
                    <iframe
                        width="600"
                        height="450"
                        frameBorder="0"
                        style={{ border: 0 }}
                        src={`https://www.google.com/maps/embed/v1/place?key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}&q=${venue.address}`}
                        allowFullScreen
                    ></iframe>
                </div> */}
            </div>
        </div>
    );
}