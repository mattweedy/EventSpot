import React, { useState } from 'react';

export default function GenreCheckbox({ genre, handleFormChange }) {
    const [isSelected, setIsSelected] = useState(false);

    const handleClick = () => {
        setIsSelected(!isSelected);
        handleFormChange('selectedGenres', genre, !isSelected);
    };

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