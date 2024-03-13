import React, { useState } from 'react';

export default function VenueCheckbox({ venue, handleFormChange, formData }) {
    const [isSelected, setIsSelected] = useState(false);

    const handleClick = () => {
        if (formData.selectedVenues.length < 5 || isSelected) {
            // Change the state
            setIsSelected(!isSelected);
            // Update the formData
            handleFormChange("selectedVenues", venue.name, !isSelected);
        } else {
            // If the limit is reached, do not add the venue
            alert('You can only select up to 5 venues.');
        }
    };

    return (
        <button
            type="button"
            key={venue.id} 
            className={`venueCheckbox ${isSelected ? 'selected' : ''}`} 
            onClick={handleClick}
        >
            {venue.name}
        </button>
    );
}