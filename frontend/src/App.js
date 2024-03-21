import './App.css';
import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Login from './components/Login/Login';
// import Logout from './components/Login/Logout';
import Header from './components/General/Header';
import QuizForm from './components/Quiz/QuizForm';
import Sidebar from './components/Sidebar/Sidebar';
import RecommendedEvents from './components/EventDetails/RecommendedEvents';
import DisplayEventVenueData from './components/Data/DisplayEventVenueData';

// TODO: allow for regenerating recommendations(?) - give next 10 recommendations instead
// TODO: Implement a loading spinner for when the app is fetching data from the backend

function App() {
    const [isLoading, setIsLoading] = useState(true);
    const [accessToken, setAccessToken] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userProfile, setUserProfile] = useState(null);
    const [isFetchingTopItems, setIsFetchingTopItems] = useState({ tracks: false, artists: false });
    const [isFetchingUserProfile, setIsFetchingUserProfile] = useState(false);
    const [recommendedEventIds, setRecommendedEventIds] = useState([]);
    const [isFormSubmitted, setIsFormSubmitted] = useState(false);
    const [isFormShown, setIsFormShown] = useState(false);
    const [isEventsVisible, setIsEventsVisible] = useState(false);


    useEffect(() => {
        window.onbeforeunload = function () {
            sessionStorage.clear();
        };

        // cleanup function
        return () => {
            window.onbeforeunload = null;
        };
    }, []);


    const fetchUserProfile = useCallback(async () => {
        if (accessToken && !isFetchingUserProfile) {
            setIsFetchingUserProfile(true);
            setIsLoading(true);
            console.log("USER PROFILE : sending backend request to spotify/profile...");
            axios.get('http://localhost:8000/spotify/profile', {
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            })
                .then(response => {
                    console.log("USER PROFILE : User profile data received from backend:", response.data);
                    setUserProfile(response.data);
                    setIsLoggedIn(true);
                })
                .catch(error => {
                    console.error("USER PROFILE : Error fetching user profile:", error);
                    setIsLoggedIn(false);
                })
                .finally(() => {
                    setIsLoading(false);
                });
        }
    }, [accessToken, isFetchingUserProfile]);

    useEffect(() => {
        setIsFetchingUserProfile(false);
    }, [accessToken]);


    useEffect(() => {
        // fetch access token from backend when component mounts
        setIsLoading(true);
        console.log("LOGGING IN : sending backend request to spotify/logged_in...");
        axios.get('http://localhost:8000/spotify/logged_in')
            .then(response => {
                if (!response.data.isLoggedIn) {
                    console.log("LOGGED OUT : Response from /spotify/logged_in:", response);
                    console.log("LOGGED OUT : User not logged in");
                    setAccessToken(null);
                    setUserProfile(null);
                    setIsLoggedIn(false);
                    return;
                } else {
                    console.log("LOGGED IN : Response from /spotify/logged_in:", response.data);
                    console.log("LOGGED IN : User logged in");
                    setAccessToken(response.data.accessToken);
                }
            })
            .finally(() => {
                setIsLoading(false);
            });
    }, []);


    const fetchTopItems = useCallback(async (type) => {
        if (accessToken && !isFetchingTopItems[type]) {
            setIsFetchingTopItems(prevState => ({ ...prevState, [type]: true }));
            let limit = 25;
            let items = [];
            for (let i = 0; i < 4; i++) {
                try {
                    const response = await axios.get(`http://localhost:8000/spotify/top/${type}?limit=${limit}&offset=${i * 25}&username=${userProfile.display_name}`, {
                        headers: {
                            'Authorization': `Bearer ${accessToken}`
                        }
                    });
                    console.log(`Successfully fetched page ${i + 1} of top ${type} from backend.`, response.data.items, "items");
                    items = items.concat(response.data.items);
                } catch (error) {
                    console.error(`Error fetching page ${i + 1} of top ${type} from backend:`, error);
                }
            }
            console.log(`Total number of top ${type} fetched: ${items.length}`);
        }
    }, [accessToken, userProfile, isFetchingTopItems]);


    useEffect(() => {
        setIsFetchingTopItems(prevState => ({ ...prevState, tracks: false }));
    }, [userProfile]);


    useEffect(() => {
        fetchUserProfile();
    }, [accessToken, fetchUserProfile]);


    useEffect(() => {
        if (userProfile) {
            fetchTopItems('tracks');
            fetchTopItems('artists');
            // fetchArtistGenres();
        }
    }, [userProfile, fetchTopItems]);

    // use effect to log to console recommendedEventIds
    useEffect(() => {
        console.log("Is Form Submitted: ", isFormSubmitted);
        console.log("Recommended Event Ids: ", recommendedEventIds);
    }, [isFormSubmitted, recommendedEventIds]);


    // if user is logged in, display the user's name
    if (isLoggedIn) {
        if (isLoading) {
            return (
                <div className="loading">
                    <h1 className="loading-text">Loading...</h1>
                    {console.log("Loading...")}
                </div>
            );
        }
        if (accessToken && userProfile && !isLoading) {
            return (
                <div className="papp">
                    <Header
                        userProfile={userProfile}
                        isLoggedIn={isLoggedIn}
                    />
                    <div className="app-content">
                        <Sidebar />
                        <button onClick={() => setIsEventsVisible(!isEventsVisible)}>
                            {isEventsVisible ? 'Hide Events and Venues' : 'Show Events and Venues'}
                        </button>
                        <main className="app-main">
                            <div className="app-body">
                                {/* TODO: Implement showing users 10 fav tracks/artists on their profile component or main page */}
                                <br></br>
                                <DisplayEventVenueData isEventsVisible={isEventsVisible} />
                                <br></br>
                                {isFormShown ? (
                                    <button onClick={() => setIsFormShown(false)}>Hide Preferences Quiz</button>
                                ) : (
                                    <button onClick={() => setIsFormShown(true)}>Edit Preferences</button>
                                )}
                                {isFormShown && (
                                    <QuizForm
                                        username={userProfile.display_name}
                                        recommendedEventIds={recommendedEventIds}
                                        setRecommendedEventIds={setRecommendedEventIds}
                                        setIsFormSubmitted={setIsFormSubmitted}
                                    />
                                )}
                            </div>
                        </main>
                    </div>
                </div>
            );
        }
    } else {
        // TODO: improve login page styling
        return (
            <div className="app">
                <Header isLoggedIn={isLoggedIn} />
                <div className="app-content">
                    <main className="app-main">
                        <Login />
                    </main>
                </div>
            </div>
        );
    }
}

export default App;
