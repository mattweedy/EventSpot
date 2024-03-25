import React, { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';

export default function GenreCheckbox({ genre, handleFormChange, formData }) {
    const [isSelected, setIsSelected] = useState(false);

    useEffect(() => {
        // check if genre is in selectedGenres array when formData changes
        setIsSelected(formData.selectedGenres.includes(genre));
    }, [formData, genre]);

    const handleClick = () => {
        if (formData.selectedGenres.length < 5 || isSelected) {
            // change the state
            setIsSelected(!isSelected);
            // update the formData
            handleFormChange("selectedGenres", genre, !isSelected);
        } else {
            // if the limit is reached, do not add the genre
            showToast('You can only select up to 5 genres.');
        }
    }


    const showToast = (message) => {
        toast.error(message, {
            style: {
                borderRadius: '10px',
                background: '#333',
                color: '#fff',
            },
        });
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