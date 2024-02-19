import React, { useEffect, useState } from 'react';
// basic react login UI component for user login using spotfiy PKCE flow
// uses the spotify web api to authenticate the user and get the access token
// and refresh token

function Login() {
    // Add your login UI component code here
    useEffect(() => {
        // code to run on component mount
        // check if the user is already logged in
        // if the user is already logged in, redirect to the home page
        // if the user is not logged in, show the login UI
    }, []);

    useState(() => {
        // Add your login UI component code here
        // check if the user is already logged in
        // if the user is already logged in, redirect to the home page
        // if the user is not logged in, show the login UI
    });

    return (
        // JSX code for the login UI
        
        <div>
            <h1>Login</h1>
            <button>Login with Spotify</button>
        </div>

    );
}

export default Login;
