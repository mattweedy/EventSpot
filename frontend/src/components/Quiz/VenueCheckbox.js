export default function VenueCheckbox({ venue, handleFormChange }) {
    return (
        <div key={venue.id} className="venueCheckbox">
            <label>
                <input
                    type="checkbox"
                    onChange={handleFormChange}
                    name="selectedVenues"
                    value={venue.name}
                />
                {venue.name}
            </label>
        </div>
    );
}