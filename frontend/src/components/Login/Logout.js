import React from 'react';
// import axios from 'axios';

// basic react login UI component for user logout
// uses the spotify web api to logout the user
// and clear the access token and refresh token

function Logout() {
    const handleLogout = async () => {
        try{
            window.location.href = 'http://localhost:8000/spotify/logout';
        } catch (error) {
            console.error("Error logging out:", error);
        }
    };

    return (
        <button onClick={handleLogout}>Logout</button>
    );
}

export default Logout;
