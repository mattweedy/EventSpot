import React, { useEffect, useState } from 'react';
// basic react login UI component for user login using spotfiy PKCE flow
// uses the spotify web api to authenticate the user and get the access token
// and refresh token

function Login() {
    // Add login UI component code here
    const handleLogin = () => {
        // Handle login logic here...
        window.location.href = 'http://localhost:8000/api/spotify/login';
    };

    useEffect(() => {
        // code to run on component mount
        // check if the user is already logged in
        // if the user is already logged in, redirect to the home page
        // if the user is not logged in, show the login UI
    }, []);

    useState(() => {
        // Add login UI component code here
        // check if the user is already logged in
        // if the user is already logged in, redirect to the home page
        // if the user is not logged in, show the login UI
    });

    return (
        <button onClick={handleLogin}>Login to Spotify</button>
    );
}

export default Login;
