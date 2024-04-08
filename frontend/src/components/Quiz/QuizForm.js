import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import PriceRange from "./PriceRange";
import VenueCheckbox from "./VenueCheckbox";
import GenreCheckbox from "./GenreCheckbox";
import SearchBar from "../General/SearchBar";
import useFetchData from "../Data/useFetchData";
import { toast } from 'react-hot-toast';

// TODO: handle cities

export default function QuizForm({ username, setRecommendedEventIds }) {
    const initialNumVenuesToShow = 35;
    // const genres = ['techno', 'rave', 'house', 'trance', 'dubstep', 'drum and bass', 'gabber', 'hardgroove', 'hardstyle', 'psytrance', 'synthpop', 'trap', 'hip hop', 'hiphop', 'rap', 'pop', 'dance', 'rock', 'metal', 'hard rock', 'country', 'bluegrass', 'jazz', 'blues', 'classical', 'orchestral', 'electronic', 'edm', 'indie', 'alternative', 'folk', 'acoustic', 'r&b', 'soul', 'reggae', 'ska', 'punk', 'emo', 'latin', 'salsa', 'gospel', 'spiritual', 'funk', 'disco', 'world', 'international', 'new age', 'ambient', 'soundtrack', 'score', 'comedy', 'parody', 'spoken word', 'audiobook', 'children\'s', 'kids', 'holiday', 'christmas', 'easy listening', 'mood', 'brazilian', 'samba', 'fado', 'portuguese', 'tango', 'grunge', 'street', 'argentinian'];
    const genres = ['acoustic', 'alternative', 'ambient', 'ambient / new age', 'americana', 'argentinian', 'baroque', 'bass', 'black metal', 'bluegrass', 'blues', 'brazilian', 'chillout', 'christian', 'classic rock', 'classical', 'comedy', 'country', 'dance', 'death metal', 'deephouse', 'disco', 'downtempo', 'drum and bass', 'dub', 'dubstep', 'easy listening', 'edm', 'electronic', 'electronic dance', 'electropop', 'emo', 'ethnic', 'fado', 'folk', 'folk rock', 'funk', 'funk / disco', 'gabber', 'ghettotech', 'global', 'gospel', 'gospel / spiritual', 'groove', 'grunge', 'hard rock', 'hardcore', 'hardgroove', 'hardstyle', 'heavy metal', 'hip hop', 'hip hop / rap', 'hiphop', 'house', 'indie', 'indie rock', 'indiepop', 'international', 'jazz', 'jazz fusion', 'latin', 'lo-fi', 'melodictechno', 'metal', 'mood', 'motown', 'new age', 'opera', 'orchestral', 'parody', 'pop', 'portuguese', 'psychedelic', 'psytrance', 'punk', 'punk / emo', 'r&b', 'rap', 'rave', 'reggae', 'reggaeton', 'rhythm and blues', 'rock', 'rocksteady', 'salsa', 'samba', 'score', 'singer-songwriter', 'ska', 'skate punk', 'smooth jazz', 'soul', 'soul / r&b', 'soundtrack', 'spiritual', 'street', 'swing', 'symphony', 'synthpop', 'tango', 'techhouse', 'techno', 'trance', 'trap', 'world', 'worship']
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
    const [readyForNavigation, setReadyForNavigation] = useState(false);
    const [showConfirmation, setShowConfirmation] = useState(false);

    const filteredVenues = venues ? venues.filter(venue => venue.name.toLowerCase().includes(venueSearchTerm.toLowerCase())) : [];
    const filteredGenres = genres ? genres.filter(genre => genre.toLowerCase().includes(genreSearchTerm.toLowerCase())) : [];
    const toastOptions = {
        style: {
            borderRadius: '10px',
            background: '#333',
            color: '#fff',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '16px',
            fontSize: '1.2em',
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
                    console.log("Previous preferences: ", response.data.data);
                    const data = response.data.data;
                    setFormData({
                        username: username,
                        selectedVenues: JSON.parse(data.venue_preferences.replace(/'/g, '"')),
                        // selectedVenues: JSON.parse(data.venue_preferences.replace(/'/g, '"')).map(venue => venue.replace(/'/g, '')),
                        selectedGenres: JSON.parse(data.genre_preferences.replace(/'/g, '"')),
                        // selectedGenres: JSON.parse(data.genre_preferences.replace(/'/g, '"')).map(genre => genre.replace(/'/g, '')),
                        priceRange: JSON.parse(data.price_range.replace(/'/g, '"')),
                        city: data.city || '',
                    });
                } else {
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
        // remove [ and ] from the value
        // value = value.replace(/[\[\]]/g, '');

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


    // fetch events based on recommendations
    const fetchEventsBasedOnRecommendations = (recommendations) => {
        // Fetch events logic
        return axios.get('http://localhost:8000/api/events')
            .then(response => {
                const allEvents = response.data;
                let events = allEvents.filter(e => recommendations.includes(e.event_id));
                events.sort((a, b) => recommendations.indexOf(a.event_id) - recommendations.indexOf(b.event_id));
                return events; // return filtered and sorted events
            })
            .catch(error => {
                console.error('Failed to filter events:', error);
                throw error; // re-throw to handle in the calling function
            });
    };

    // store the recommended event in local storage
    const storeEventsInLocalStorage = (events) => {
        // console.log("Setting recommendedEvents to storage:", events);
        localStorage.setItem('recommendedEvents', JSON.stringify(events));
        // console.log("Set recommendedEvents to storage:", events);
    };

    const processAndNavigateRecommendations = () => {
        axios.get(`http://localhost:8000/api/recommendations?username=${formData.username}`)
            .then(response => {
                const recommendations = response.data.recommendations;
                fetchEventsBasedOnRecommendations(recommendations)
                    .then(events => {
                        storeEventsInLocalStorage(events);
                        setRecommendedEventIds(recommendations);
                        setReadyForNavigation(true); // this triggers the useEffect to navigate
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
        toast("No changes made", toastOptions);
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
            <p>Hitting <span>save</span> will redirect you to the recommended events page</p>
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
            {/* <input
                type="radio"
                onChange={handleFormChange}
                name="city"
            /> */}
            <PriceRange
                formData={formData}
                setValues={handlePriceRangeChange}
            />
            <br></br>
            <button type="submit" className="preferences-form-button">Save</button>
        </form>
    );
}