import React, { useState, useEffect } from 'react';

export default function GenreCheckbox({ genre, handleFormChange, formData }) {
    const [isSelected, setIsSelected] = useState(false);

    useEffect(() => {
        // check if genre is in selectedGenres array when formData changes
        setIsSelected(formData.selectedGenres.includes(genre));
    }, [formData, genre]);

    const handleClick = () => {
        if (formData.selectedGenres.length < 5 || isSelected) {
            // Change the state
            setIsSelected(!isSelected);
            // Update the formData
            handleFormChange("selectedGenres", genre, !isSelected);
        } else {
            // If the limit is reached, do not add the genre
            alert('You can only select up to 5 genres.');
        }
    }

    return (
        <button
            type="button"
            key={genre} 
            className={`genreCheckbox ${isSelected ? 'selected' : ''}`} 
            onClick={handleClick}
        >
            {genre}
        </button>
    );
}