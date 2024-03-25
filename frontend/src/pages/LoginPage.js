import React from 'react';
import Login from '../components/Login/Login';

const LoginPage = () => {
    return (
        <div className="login-page">
            <div className="login-page-container">
                <h1>Welcome to Spot<span>Event</span></h1>
                <div id="login-page-dialog">
                    <h2>This application allows you to explore and discover upcoming events that
                        closely match your music taste and preferences.
                    </h2>
                </div>
                <p>To begin, simply login through Spotify</p>
            </div>
            <Login />
        </div>
    );
};

export default LoginPage;