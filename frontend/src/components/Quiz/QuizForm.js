import React, { useState } from "react";
import PriceRange from "./PriceRange";

export default function QuizForm() {
    // TODO: figure out how to handle the selectedVenues and selectedGenres fields
    const [formData, setFormData] = useState({
        selectedVenues: [],
        selectedGenres: [],
        priceRange: [0, 100], // this is a range
        queerPreference: '', // more / less / no preference
        howSoon: '', // this is a date field(?)
        city: '', // maybe use a dropdown
    });

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

    // TODO: store the form data in user preferences


    // TODO: insert price range component
    // TODO: handle cities
    return (
        <form>
            <input
                type="checkbox"
                onChange={handleFormChange}
                name="selectedVenues"
            />
            <input
                type="checkbox"
                onChange={handleFormChange}
                name="selectedGenres"
            />
            {/* TODO: insert price range component */}
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
        </form>
    );
}