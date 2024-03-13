import React, { useEffect, useState } from "react";
import axios from "axios";
import PriceRange from "./PriceRange";
import VenueCheckbox from "./VenueCheckbox";
import useFetchData from "../Data/useFetchData";

// TODO: generate venues selection buttons (venue names) from database (use useFetchData)
// TODO: handle cities


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
    const venueData = useFetchData('/venues/');
    const [venues, setVenues] = useState([]);

    useEffect(() => {
        setFormData(prev => ({
            ...prev,
            username: username
        }));
    }, [username]);

    useEffect(() => {
        setVenues(venueData);
    }, [venueData]);

    const handleFormChange = (e) => {
        const { name, value, checked } = e.target;

        setFormData(prev => {
            if (name === "selectedVenues") {
                if (checked) {
                    // If the checkbox is checked, add the venue to the array
                    return { ...prev, [name]: [...prev[name], value] };
                } else {
                    // If the checkbox is unchecked, remove the venue from the array
                    return { ...prev, [name]: prev[name].filter(venue => venue !== value) };
                }
            } else {
                return { ...prev, [name]: value };
            }
        });
    };

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


    return (
        <form onSubmit={handleSubmit}>
            {venues && venues.map(venue => (
            <VenueCheckbox
                key={venue.id}
                venue={venue}
                handleFormChange={handleFormChange}
            />
            ))}
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