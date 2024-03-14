import React, { useEffect, useState } from "react";
import axios from "axios";
import PriceRange from "./PriceRange";
import VenueCheckbox from "./VenueCheckbox";
import GenreCheckbox from "./GenreCheckbox";
import useFetchData from "../Data/useFetchData";

// ! This component is not complete

// TODO: change alerts to something more user-friendly (e.g. a message on the page)

// TODO: handle queerPreference
// TODO: handle howSoon
// TODO: handle cities


export default function QuizForm({ username, setRecommendedEventIds, setIsFormSubmitted,}) {
    const genres = ['techno', 'rave', 'house', 'trance', 'dubstep', 'drum and bass', 'gabber', 'hardgroove', 'hardstyle', 'psytrance', 'synthpop', 'trap', 'hip hop', 'hiphop', 'rap', 'pop', 'dance', 'rock', 'metal', 'hard rock', 'country', 'bluegrass', 'jazz', 'blues', 'classical', 'orchestral', 'electronic', 'edm', 'indie', 'alternative', 'folk', 'acoustic', 'r&b', 'soul', 'reggae', 'ska', 'punk', 'emo', 'latin', 'salsa', 'gospel', 'spiritual', 'funk', 'disco', 'world', 'international', 'new age', 'ambient', 'soundtrack', 'score', 'comedy', 'parody', 'spoken word', 'audiobook', 'children\'s', 'kids', 'holiday', 'christmas', 'easy listening', 'mood', 'brazilian', 'samba', 'fado', 'portuguese', 'tango', 'grunge', 'street', 'argentinian'];
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
    const [numVenuesToShow, setNumVenuesToShow] = useState(25);

    useEffect(() => {
        setFormData(prev => ({
            ...prev,
            username: username
        }));
    }, [username]);


    useEffect(() => {
        setVenues(venueData);
    }, [venueData]);


    const handleFormChange = (name, value, isSelected) => {
        setFormData(prev => {
            if (name === "selectedVenues") {
                if (isSelected) {
                    // If the checkbox is selected and the limit is not reached, add the venue to the array
                    if (prev[name].length < 5) {
                        return { ...prev, [name]: [...prev[name], value] };
                    } else {
                        // If the limit is reached, do not add the venue
                        return prev;
                    }
                } else {
                    // If the checkbox is deselected, remove the venue from the array
                    return { ...prev, [name]: prev[name].filter(item => item !== value) };
                }
            } else if (name === "selectedGenres") {
                if (isSelected) {
                    // If the checkbox is selected and the limit is not reached, add the genre to the array
                    if (prev[name].length < 5) {
                        return { ...prev, [name]: [...prev[name], value] };
                    } else {
                        // If the limit is reached, do not add the genre
                        return prev;
                    }
                } else {
                    // If the checkbox is deselected, remove the genre from the array
                    return { ...prev, [name]: prev[name].filter(item => item !== value) };
                }
            } else {
                // For other form fields, just update the value
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

            // call the get_recommendations endpoint
            return axios.get(`http://localhost:8000/api/recommendations?username=${formData.username}`);
        })
        .then(response => {
            // update the state with the recommended event ids
            setRecommendedEventIds(response.data.recommendations);
        })
        .catch(error => {
            console.error(error);
        });

        setIsFormSubmitted(true);
    }


    const handleDisplayMore = () => {
        setNumVenuesToShow(venues.length);
    };


    // const genreCheckboxes = genres.map(genre => (
    //     <GenreCheckbox
    //         key={genre}
    //         genre={genre}
    //         isSelected={formData.selectedGenres.includes(genre)}
    //         onGenreClick={() => handleGenreClick(genre)}
    //     />
    // ));

    // const venueCheckboxes = venues.slice(0, numVenuesToShow).map(venue => (
    //     <VenueCheckbox
    //         key={venue.id}
    //         venue={venue}
    //         handleFormChange={handleFormChange}
    //         onClick={() => handleVenueClick(venue)}
    //         // formData={formData}
    //     />
    // ));


    return (
        <form onSubmit={handleSubmit}>
            <div className="box" id="venues">
                <h3>Choose <span>3-5</span> of your favourite Venues</h3>
                <h4>Previous choices: {formData.selectedGenres}</h4>
                {venues && venues.slice(0, numVenuesToShow).map(venue => (
                    <VenueCheckbox
                        key={venue.id}
                        venue={venue}
                        handleFormChange={handleFormChange}
                        formData={formData}
                    />
                ))}
                {venues && numVenuesToShow < venues.length && (
                    <button onClick={handleDisplayMore} className="displayMore">Display All</button>
                )}
            </div>
            <div className="box" id="genres">
                <h3>Choose up to <span>5</span> of your favourite Genres</h3>
                {genres.map(genre => (
                    <GenreCheckbox
                        key={genre}
                        genre={genre}
                        handleFormChange={handleFormChange}
                        formData={formData}
                    />
                ))}
            </div>
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