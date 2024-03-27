import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import PriceRange from "./PriceRange";
import VenueCheckbox from "./VenueCheckbox";
import GenreCheckbox from "./GenreCheckbox";
import SearchBar from "../General/SearchBar";
import useFetchData from "../Data/useFetchData";
import { toast } from 'react-hot-toast';

// ! This component is not complete

// TODO: in logout, clear the local storage
// TODO: make sure handleSkip does same saving of recommended events as handleSubmit
// TODO: handle cities

export default function QuizForm({ username, recommendedEventIds, setRecommendedEventIds }) {
    const initialNumVenuesToShow = 35;
    const genres = ['techno', 'rave', 'house', 'trance', 'dubstep', 'drum and bass', 'gabber', 'hardgroove', 'hardstyle', 'psytrance', 'synthpop', 'trap', 'hip hop', 'hiphop', 'rap', 'pop', 'dance', 'rock', 'metal', 'hard rock', 'country', 'bluegrass', 'jazz', 'blues', 'classical', 'orchestral', 'electronic', 'edm', 'indie', 'alternative', 'folk', 'acoustic', 'r&b', 'soul', 'reggae', 'ska', 'punk', 'emo', 'latin', 'salsa', 'gospel', 'spiritual', 'funk', 'disco', 'world', 'international', 'new age', 'ambient', 'soundtrack', 'score', 'comedy', 'parody', 'spoken word', 'audiobook', 'children\'s', 'kids', 'holiday', 'christmas', 'easy listening', 'mood', 'brazilian', 'samba', 'fado', 'portuguese', 'tango', 'grunge', 'street', 'argentinian'];
    const [formData, setFormData] = useState({
        username: username,
        selectedVenues: [],
        selectedGenres: [],
        priceRange: [0, 100], // this is a range
        city: '', // maybe use a dropdown
    });
    const venueData = useFetchData('/venues/');
    const [venues, setVenues] = useState([]);
    const [numVenuesToShow, setNumVenuesToShow] = useState(initialNumVenuesToShow);
    const [venueSearchTerm, setVenueSearchTerm] = useState('');
    const [genreSearchTerm, setGenreSearchTerm] = useState('');
    const [previousPreferences, setPreviousPreferences] = useState(false);
    const [readyForNavigation, setReadyForNavigation] = useState(false);

    const filteredVenues = venues ? venues.filter(venue => venue.name.toLowerCase().includes(venueSearchTerm.toLowerCase())) : [];
    const filteredGenres = genres ? genres.filter(genre => genre.toLowerCase().includes(genreSearchTerm.toLowerCase())) : [];
    const toastOptions = {
        style: {
            borderRadius: '10px',
            background: '#333',
            color: '#fff',
            alignItems: 'center',
            justifyContent: 'center',
        },
        duration: 6000,
    };
    const navigate = useNavigate();

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
                    console.log("Previous preferences: ", response.data.data);
                    console.log("Venue preferences: ", response.data.data.venue_preferences);
                    setFormData({
                        username: username,
                        selectedVenues: response.data.data.venue_preferences,
                        selectedGenres: response.data.data.genre_preferences,
                        priceRange: response.data.data.price_range,
                        city: response.data.data.city,
                    });
                } else {
                    setPreviousPreferences(false);
                    // if user had no previous preferences, set formData to default values
                    setFormData({
                        username: username,
                        selectedVenues: [],
                        selectedGenres: [],
                        priceRange: [0, 100],
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
                    // if the checkbox is selected and the limit is not reached, add the venue to the array
                    if (prev[name].length < 5) {
                        return { ...prev, [name]: [...prev[name], value] };
                    } else {
                        // if the limit is reached, do not add the venue
                        return prev;
                    }
                } else {
                    // if the checkbox is deselected, remove the venue from the array
                    return { ...prev, [name]: prev[name].filter(item => item !== value) };
                }
            } else if (name === "selectedGenres") {
                if (isSelected) {
                    // if the checkbox is selected and the limit is not reached, add the genre to the array
                    if (prev[name].length < 5) {
                        return { ...prev, [name]: [...prev[name], value] };
                    } else {
                        // if the limit is reached, do not add the genre
                        return prev;
                    }
                } else {
                    // if the checkbox is deselected, remove the genre from the array
                    return { ...prev, [name]: prev[name].filter(item => item !== value) };
                }
            } else {
                // for other form fields, just update the value
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

    // _________________________________________________________


        // fetch events based on recommendations
    const fetchEventsBasedOnRecommendations = (recommendedEventIds) => {
        // Fetch events logic
        return axios.get('http://localhost:8000/api/events')
            .then(response => {
                const allEvents = response.data;
                let events = allEvents.filter(e => recommendedEventIds.includes(e.event_id));
                events.sort((a, b) => recommendedEventIds.indexOf(a.event_id) - recommendedEventIds.indexOf(b.event_id));
                return events; // Return filtered and sorted events
            })
            .catch(error => {
                console.error('Failed to filter events:', error);
                throw error; // Re-throw to handle in the calling function
            });
    };

    // store the recommended event in local storage
    const storeEventsInLocalStorage = (events) => {
        console.log("Setting recommendedEvents to storage:", events);
        localStorage.setItem('recommendedEvents', JSON.stringify(events));
        console.log("Set recommendedEvents to storage:", events);
    };

    const processAndNavigateRecommendations = () => {
        axios.get(`http://localhost:8000/api/recommendations?username=${formData.username}`)
            .then(response => {
                const recommendations = response.data.recommendations;
                fetchEventsBasedOnRecommendations(recommendations)
                    .then(events => {
                        storeEventsInLocalStorage(events);
                        setRecommendedEventIds(recommendations);
                        setReadyForNavigation(true); // This triggers the useEffect to navigate
                    }).catch(error => {
                        console.error('Error fetching events based on recommendations:', error);
                        showToast('An error occurred. Please try again.', 'error');
                    });
            })
            .catch(error => {
                console.error('Error fetching recommendations:', error);
                showToast('An error occurred while fetching recommendations. Please try again.', 'error');
            });
    };

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
    
        if (data.venuePreferences.length > 0 || data.genrePreferences.length > 0 || data.priceRange.length > 0 || data.queerPreference !== null || data.howSoon !== null || data.city !== null) {
            axios.post('http://localhost:8000/api/set_preferences', data)
                .then(() => processAndNavigateRecommendations())
                .catch(error => {
                    console.error('Error setting preferences:', error);
                    showToast('An error occurred while saving preferences. Please try again.', 'error');
                });
        } else {
            processAndNavigateRecommendations();
        }
    };

    const handleSkip = () => {
        processAndNavigateRecommendations();
    };


    useEffect(() => {
        if (readyForNavigation) {
            navigate('/recommended-events');
            setReadyForNavigation(false);
        }
    }, [readyForNavigation, navigate]);

    // _________________________________________________________

    // ! OG handleSubmit
    // const handleSubmit = (event) => {
    //     event.preventDefault();

    //     const data = {
    //         username: formData.username,
    //         venuePreferences: formData.selectedVenues,
    //         genrePreferences: formData.selectedGenres,
    //         priceRange: formData.priceRange,
    //         queerPreference: formData.queerPreference,
    //         howSoon: formData.howSoon,
    //         city: formData.city,
    //     };

    //     // check if any preferences have been changed
    //     if (data.venuePreferences.length > 0 || data.genrePreferences.length > 0 || data.priceRange.length > 0 || data.queerPreference !== null || data.howSoon !== null || data.city !== null) {
    //         // if any preferences have been changed, set the new preferences
    //         axios.post('http://localhost:8000/api/set_preferences', data)
    //             .then(response => {
    //                 console.log("response:", response);

    //                 // call the get_recommendations endpoint
    //                 return axios.get(`http://localhost:8000/api/recommendations?username=${formData.username}`);
    //             })
    //             .then(response => {
    //                 // update the state with the recommended event ids
    //                 setRecommendedEventIds(response.data.recommendations);
    //             })
    //             .catch(error => {
    //                 console.error(error);
    //                 showToast('An error occurred. Please try again.', 'error');
    //             })
    //             .finally(() => {
    //                 // show toast notification
    //                 showToast('Preferences saved!', 'success');
    //                 navigate('/recommended-events');
    //             });
    //     } else {
    //         // if no preferences have been changed, just get the recommendations
    //         axios.get(`http://localhost:8000/api/recommendations?username=${formData.username}`)
    //             .then(response => {
    //                 // update the state with the recommended event ids
    //                 setRecommendedEventIds(response.data.recommendations);
    //             })
    //             .catch(error => {
    //                 console.error(error);
    //                 showToast('An error occurred. Please try again.', 'error');
    //             })
    //             .finally(() => {
    //                 // show toast notification
    //                 showToast('Preferences saved!', 'success');
    //                 navigate('/recommended-events');
    //             });
    //     }
    // }





    const showToast = (message, type) => {
        if (type === 'success') {
            toast.success(message, toastOptions);
        } else if (type === 'error') {
            toast.error(message, toastOptions);
        }
    }


    const showUndoToast = () => {
        toast((t) => (
            <div>
                Undo changes?
                <button onClick={() => {
                    axios.get(`http://localhost:8000/api/get_preferences?username=${username}`)
                        .then(response => {
                            setFormData({
                                username: username,
                                selectedVenues: response.data.data.venue_preferences || [],
                                selectedGenres: response.data.data.genre_preferences || [],
                                priceRange: response.data.data.price_range || [0, 100],
                                queerPreference: response.data.data.queer_events || '',
                                howSoon: response.data.data.how_soon || '',
                                city: response.data.data.city || '',
                            })
                        });
                    toast.success("Preferences restored successfully", toastOptions);
                }} className="preferences-form-button" style={{ margin: '0px 5px 0px 10px', height: '30px' }}>Undo</button>
                <button onClick={() => {
                    toast.dismiss(t.id);
                    toast.success("Preferences cleared!", toastOptions);
                }} className="preferences-form-button" style={{ margin: '0px 0px 0px 5px', height: '30px' }}>Dismiss</button>
            </div>
        ), toastOptions)
    }


    // ! OG handleSkip
    // const handleSkip = () => {
    //     if (!previousPreferences) {
    //         // if the user doesn't have previous preferences, submit the form with no preferences
    //         axios.post('http://localhost:8000/api/submit_form', formData)
    //             .then(response => {
    //                 setRecommendedEventIds(response.data.data);
    //             })
    //             .catch(error => {
    //                 console.error(error);
    //             })
    //             .finally(() => {
    //                 navigate('/recommended-events');
    //             });
    //     } else {
    //         // if the user has previous preferences, just fetch the recommended events
    //         axios.get(`http://localhost:8000/api/recommendations?username=${username}`)
    //             .then(response => {
    //                 setRecommendedEventIds(response.data.data);
    //             })
    //             .catch(error => {
    //                 console.error(error);
    //             })
    //             .finally(() => {
    //                 navigate('/recommended-events');
    //             });
    //     }
    // };


    // useEffect(() => {
    //     if (readyForNavigation) {
    //         navigate('/recommended-events');
    //         setReadyForNavigation(false);
    //     }
    // }, [readyForNavigation, navigate]);


    const resetFormData = () => {
        // showToast
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


    const [showConfirmation, setShowConfirmation] = useState(false);

    const handleClearPreferences = () => {
        setShowConfirmation(true);
    };

    const handleConfirmationYes = () => {
        resetFormData();
        setShowConfirmation(false);
        showUndoToast();
    };

    const handleConfirmationNo = () => {
        setShowConfirmation(false);
    };

    return (
        <form onSubmit={handleSubmit} className="preferences-form">
            <button type="button" onClick={handleSkip} className="preferences-form-button">Skip</button>
            <button type="button" onClick={handleClearPreferences} className="preferences-form-button">Clear Preferences</button>
            {showConfirmation && (
                <div className="confirmation">
                    <p>Are you sure you want to clear your preferences?</p>
                    <button onClick={handleConfirmationYes} className="preferences-form-button">Yes</button>
                    <button onClick={handleConfirmationNo} className="preferences-form-button">No</button>
                </div>
            )}
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
                    <button type="button" onClick={handleDisplayMore} className="preferences-form-button" id="displayMore">
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
            <br></br>
            {/* TODO: figure out how to handle cities... do i take the text input and do eventbrite requests? if so only 2/3 */}
            <input
                type="radio"
                onChange={handleFormChange}
                name="city"
            />
            <PriceRange
                formData={formData}
                setValues={handlePriceRangeChange}
            />
            <br></br>
            <button type="submit" className="preferences-form-button">Save</button>
        </form>
    );
}