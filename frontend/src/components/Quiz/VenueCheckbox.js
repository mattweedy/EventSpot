import React, { useState, useEffect } from 'react';

export default function VenueCheckbox({ venue, handleFormChange, formData }) {
    const [isSelected, setIsSelected] = useState(false);

    useEffect(() => {
        // check if venue is in selectedVenues array when formData changes
        setIsSelected(formData.selectedVenues.includes(venue.name));
    }, [formData, venue.name])

    const handleClick = () => {
        if (formData.selectedVenues.length < 5 || isSelected) {
            // change the state
            setIsSelected(!isSelected);
            // update the formData
            handleFormChange("selectedVenues", venue.name, !isSelected);
        } else {
            // if the limit is reached, do not add the venue
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