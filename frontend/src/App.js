import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/Login/Login';
import Header from './components/Header';
import DisplayEventVenueData from './components/Data/DisplayEventVenueData';


function App() {
    const [accessToken, setAccessToken] = useState('');
    const [userProfile, setUserProfile] = useState(null);

    useEffect(() => {
        // fetch access token from backend when component mounts
        console.log("sending /spotify/logged_in request to backend...");
        axios.get('http://localhost:8000/spotify/logged_in')
            .then(response => {
                console.log("Response from /spotify/logged_in:", response.data);
                if (response.data.isLoggedIn) {
                    setAccessToken(response.data.accessToken);
                }
            })
            .catch(error => {
                console.error("Error fetching access token:", error);
            });
    }, []);


    useEffect(() => {
        // Fetch the user profile when the access token changes
        if (accessToken) {
            console.log("sending /spotify/profile request to backend...");
            axios.get('http://localhost:8000/spotify/profile', {
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            })
                .then(response => {
                    console.log("User profile data received from backend:", response.data);
                    setUserProfile(response.data);
                });
        }
    }, [accessToken]);

    // if user is logged in, display the user's name
    if (accessToken) {
        return (
            <div>
                <div style={{ textAlign: 'center' }}>
                    <p>{accessToken}</p>
                    <Header />
                    <h2>Welcome, {userProfile.displayName}!</h2>
                    {/* other components only for logged in */}
                    <DisplayEventVenueData />
                </div>
            </div>
        );
    } else {
        return (
            <div>
                <div style={{ textAlign: 'center' }}>
                    <Header />
                    <Login />
                </div>
            </div>
        );
    }

}

export default App;
