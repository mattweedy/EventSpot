import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Login from './components/Login/Login';
import Header from './components/Header';
import DisplayEventVenueData from './components/Data/DisplayEventVenueData';
import Logout from './components/Login/Logout';


function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [accessToken, setAccessToken] = useState('');
    const [userProfile, setUserProfile] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

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
        if (accessToken) {
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

    
    useEffect(() => {
        fetchUserProfile();
    }, [accessToken, fetchUserProfile]);


    // if user is logged in, display the user's name
    if (isLoggedIn) {
        if (isLoading) {
            return (
                <div style={{ backgroundColor: '#202020', height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center', color: '#fff' }}>
                    <h1 style={{ fontSize: '150px', color: 'red' }}>Loading...</h1>
                    {console.log("Loading...")}
                </div>
            );
        }
        if (accessToken && userProfile && !isLoading) {
            return (
                <div style={{ backgroundColor: '#202020', color: '#fff' }}>
                    {/* {userProfile.display_name} logged in
                    <div>
                        <img src={userProfile.images[0].url} alt="user profile picture" />
                    </div> */}
                    <div style={{ textAlign: 'center' }}>
                        <Header 
                            userProfile={userProfile}
                            isLoggedIn={isLoggedIn}
                        />
                        <h2>Welcome!</h2>
                        <DisplayEventVenueData />
                        <br />
                        <Logout />
                    </div>
                </div>
            );
        }
    } else {
        return (
            <div style={{ backgroundColor: '#202020', color: '#fff' }}>
                <div style={{ textAlign: 'center' }}>
                    <Header isLoggedIn={isLoggedIn}/>
                    <Login />
                </div>
            </div>
        );
    }
}

export default App;
