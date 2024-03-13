import React, { useEffect, useState } from "react";
import PriceRange from "./PriceRange";
// import useFetchData from "../Data/useFetchData";
import axios from "axios";

export default function QuizForm({ username }) {
    const [formData, setFormData] = useState({
        username: username,
        selectedVenues: [],
        selectedGenres: [],
        priceRange: [0, 100], // this is a range
        queerPreference: '', // more / less / no preference
        howSoon: '', // this is a date field(?)
        city: '', // maybe use a dropdown
    });

    useEffect(() => {
        setFormData(prev => ({
            ...prev,
            username: username
        }));
    }, [username]);

    const handleFormChange = (e) => {
        setFormData(prev => ({
            ...prev,
            [e.target.name]: e.target.value
        }));
    }

    const handlePriceRangeChange = (values) => {
        setFormData(prev => ({
            ...prev,
            priceRange: values
        }));
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        // console.log(formData);
        const data = {
            username: formData.username,
            venuePreferences: formData.selectedVenues,
            genrePreferences: formData.selectedGenres,
            priceRange: formData.priceRange,
            queerPreference: formData.queerPreference,
            howSoon: formData.howSoon,
            city: formData.city,
        };

        axios.post('http://localhost:8000/api/preferences', data)
        .then(response => {
            console.log(response);
        })
        .catch(error => {
            console.error(error);
        });
    }


    // TODO: handle cities
    return (
        <form onSubmit={handleSubmit}>
            <input className="venueCheckbox"
                type="checkbox"
                onChange={handleFormChange}
                name="selectedVenues"
            />
            <input className="genreCheckbox"
                type="checkbox"
                onChange={handleFormChange}
                name="selectedGenres"
            />
            <PriceRange
                values={formData.priceRange}
                setValues={handlePriceRangeChange}
            />
            <input
                type="radio"
                onChange={handleFormChange}
                name="queerPreference"
            />
            <input
                type="date"
                onChange={handleFormChange}
                name="howSoon"
            />
            {/* TODO: figure out how to handle cities... do i take the text input and do eventbrite requests? if so only 2/3 */}
            {/*  */}
            <input
                type="radio"
                onChange={handleFormChange}
                name="city"
            />
            <button type="submit">Submit</button>
        </form>
    );
}