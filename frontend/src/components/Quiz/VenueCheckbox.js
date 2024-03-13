import React, { useState } from 'react';

export default function VenueCheckbox({ venue, handleFormChange, formData }) {
    const [isSelected, setIsSelected] = useState(false);

    // const handleClick = () => {
    //     setIsSelected(!isSelected);
    //     handleFormChange(venue.name, !isSelected);
    // };

    // const handleClick = () => {
    //     if (formData.selectedVenues.length < 5) {
    //         // Change the state
    //         setIsSelected(!isSelected);
    //         // Update the formData
    //         handleFormChange("selectedVenues", venue.name, !isSelected);
    //         // if the limit is reached but click on button that is already selected, remove the venue from the array
    //     } else if (isSelected) {
    //         setIsSelected(!isSelected);
    //         handleFormChange("selectedVenues", venue.name, isSelected);
    //     } else {
    //         // If the limit is reached, do not add the venue
    //         alert('You can only select up to 5 venues.');
    //     }
    // };

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