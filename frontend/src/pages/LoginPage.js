import React from 'react';
import Login from '../components/Login/Login';

const LoginPage = () => {
    return (
        <div className="login-page">
                <h1 className="login-page-title">Welcome to Spot<span>Event</span></h1>
                <div className="login-page-dialog">
                    <h2 className="login-page-text">Explore and discover upcoming music events that
                        closely match <u>your</u> music taste and preferences.
                    </h2>
                    <p className="login-page-text">Spot<span>Event</span> aims to provide you with custom and personal event recommendations, based on your favourite genres gathered from your top listened tracks and artists from Spotify.</p>
                    <p className="login-page-text">After logging in, you have the option to further customise youre preferences, being able to specify some of your favourite venues and further highlight your favourite genres, or skip straight to getting recommendations.</p>
                    <p className="login-page-text">These recommendations can also be saved and removed to help improve your recommended events in the future.</p>
                    <br></br>
                    <h3 className="login-page-text">To begin, simply login with your Spotify account </h3>
                </div>
            <Login />
        </div>
    );
};

export default LoginPage;