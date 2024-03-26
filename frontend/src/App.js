import './App.css';
import React, { useState, useEffect, useCallback } from "react";
import { createBrowserRouter, RouterProvider, } from "react-router-dom";
import axios from 'axios';
import Page404 from './pages/Page404';
import routes from './routes';
import Layout from './components/General/Layout';
import Login from './components/Login/Login';
// import toast from 'react-hot-toast';


function App() {
    const [accessToken, setAccessToken] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userProfile, setUserProfile] = useState(null);
    const [isFetchingTopItems, setIsFetchingTopItems] = useState({ tracks: false, artists: false });
    const [isFetchingUserProfile, setIsFetchingUserProfile] = useState(false);
    const [recommendedEventIds, setRecommendedEventIds] = useState([]);

    // initialize a browser router
    const router = createBrowserRouter([
        {
            path: "/",
            // parent route component
            element: <Layout
                userProfile={userProfile}
                isLoggedIn={isLoggedIn}
                recommendedEventIds={recommendedEventIds}
                setRecommendedEventIds={setRecommendedEventIds}
            />,
            errorElement: <Page404 />,
            // child routes
            children: [
                ...routes
            ],
        },
        {
            path: "/login",
            element: <Login />,
        }
    ]);

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
            // setIsLoading(true);
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
                    // setIsLoading(false);
                });
        }
    }, [accessToken, isFetchingUserProfile]);

    useEffect(() => {
        setIsFetchingUserProfile(false);
    }, [accessToken]);


    useEffect(() => {
        // fetch access token from backend when component mounts
        // setIsLoading(true);
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
                // setIsLoading(false);
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
    

    return (
        <RouterProvider router={router} />
    )
}

export default App;