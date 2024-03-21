import React, { useEffect, useState } from "react";
import axios from "axios";
import SearchBar from "./SearchBar";
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
    const initialNumVenuesToShow = 25;
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
    const [numVenuesToShow, setNumVenuesToShow] = useState(initialNumVenuesToShow);
    const [venueSearchTerm, setVenueSearchTerm] = useState('');
    const [genreSearchTerm, setGenreSearchTerm] = useState('');
    const [previousPreferences, setPreviousPreferences] = useState(false);

    const filteredVenues = venues ? venues.filter(venue => venue.name.toLowerCase().includes(venueSearchTerm.toLowerCase())) : [];
    const filteredGenres = genres ? genres.filter(genre => genre.toLowerCase().includes(genreSearchTerm.toLowerCase())) : [];


    useEffect(() => {
        setFormData(prev => ({
            ...prev,
            username: username
        }));
    }, [username]);


    useEffect(() => {
        setVenues(venueData);
    }, [venueData]);


    // get the user's previous preferences (try minimise the number times preferences called)
    useEffect(() => {
        // get the user's previous preferences
        axios.get(`http://localhost:8000/api/get_preferences?username=${username}`)
            .then(response => {
                // if user had previous preferences, set previousPreferences to true
                if (response.data.data) {
                    setPreviousPreferences(true);
                    // update formData with the user's previous preferences
                    console.log("response.data.data.venuePreferences: ", response.data.data.venuePreferences);
                    setFormData({
                        username: username,
                        selectedVenues: response.data.data.venue_preferences || [],
                        selectedGenres: response.data.data.genre_preferences || [],
                        priceRange: response.data.data.price_range || [0, 100],
                        queerPreference: response.data.data.queer_events || '',
                        howSoon: response.data.data.how_soon || '',
                        city: response.data.data.city || '',
                    });
                    console.log("Previous preferences: ", response.data.data);
                    console.log("FormData: ", formData);
                } else {
                    // if user had no previous preferences, set formData to default values
                    setFormData({
                        username: username,
                        selectedVenues: [],
                        selectedGenres: [],
                        priceRange: [0, 100],
                        queerPreference: '',
                        howSoon: '',
                        city: '',
                    });
                }
            })
            .catch(error => {
                console.error(error);
            });
    // eslint-disable-next-line
    }, []); // empty dependency array means this useEffect will only run once, when the component first mounts


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

        const data = {
            username: formData.username,
            venuePreferences: formData.selectedVenues,
            genrePreferences: formData.selectedGenres,
            priceRange: formData.priceRange,
            queerPreference: formData.queerPreference,
            howSoon: formData.howSoon,
            city: formData.city,
        };

        // check if any preferences have been changed
        if (data.venuePreferences.length > 0 || data.genrePreferences.length > 0 || data.priceRange.length > 0 || data.queerPreference !== null || data.howSoon !== null || data.city !== null) {
            // if any preferences have been changed, set the new preferences
            axios.post('http://localhost:8000/api/set_preferences', data)
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
        } else {
            // if no preferences have been changed, just get the recommendations
            axios.get(`http://localhost:8000/api/recommendations?username=${formData.username}`)
                .then(response => {
                    // update the state with the recommended event ids
                    setRecommendedEventIds(response.data.recommendations);
                })
                .catch(error => {
                    console.error(error);
                });
        }
        setIsFormSubmitted(true);
    }


    const handleSkip = () => {
        if (!previousPreferences) {
            // if the user doesn't have previous preferences, submit the form with no preferences
            axios.post('http://localhost:8000/api/submit_form', formData)
                .then(response => {
                    setRecommendedEventIds(response.data.data);
                    setIsFormSubmitted(true);
                })
                .catch(error => {
                    console.error(error);
                });
        } else {
            // if the user has previous preferences, just fetch the recommended events
            axios.get(`http://localhost:8000/api/get_recommended_events?username=${username}`)
                .then(response => {
                    setRecommendedEventIds(response.data.data);
                    setIsFormSubmitted(true);
                })
                .catch(error => {
                    console.error(error);
                });
        }
    };


    const resetFormData = () => {
        setFormData({
            username: username,
            selectedVenues: [],
            selectedGenres: [],
            priceRange: [0, 100],
            queerPreference: '',
            howSoon: '',
            city: '',
        });
    }


    const handleDisplayMore = () => {
        setNumVenuesToShow(prevNum => prevNum === initialNumVenuesToShow ? venues.length : initialNumVenuesToShow);
    };

    
    return (
        <form onSubmit={handleSubmit} className="preferencesForm" id="preferencesForm">
            <button type="submit" onClick={handleSkip}>Skip</button>
            <br></br>
            <button type="button" onClick={resetFormData}>Clear Preferences</button>
            <br></br>

            <div className="box" id="venues">
                <h3>Select up to <span>5</span> of your favourite Venues</h3>
                <SearchBar searchTerm={venueSearchTerm} setSearchTerm={setVenueSearchTerm} />
                <div className="innerBox">
                    {filteredVenues.length === 0 ? <h4>Specified venue not found.</h4> : null}
                    {filteredVenues.slice(0, numVenuesToShow).map(venue => (
                        <VenueCheckbox
                            key={venue.id}
                            venue={venue}
                            handleFormChange={handleFormChange}
                            formData={formData}
                        />
                    ))}
                    <button onClick={handleDisplayMore} className="displayMore">
                        {numVenuesToShow === initialNumVenuesToShow ? 'Display All' : 'Show Less'}
                    </button>
                </div>
            </div>
            <div className="box" id="genres">
                <h3>Choose <span>5</span> of your favourite Genres</h3>
                <SearchBar searchTerm={genreSearchTerm} setSearchTerm={setGenreSearchTerm} />
                <div className="innerBox">
                    {filteredGenres.length === 0 ? <h4>Specified genre not found.</h4> : null}
                    {filteredGenres.map(genre => (
                        <GenreCheckbox
                            key={genre}
                            genre={genre}
                            handleFormChange={handleFormChange}
                            formData={formData}
                        />
                    ))}
                </div>
            </div>
            <PriceRange
                formData={formData}
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
            <br></br>
            <button type="submit">Submit</button>
        </form>
    );
}