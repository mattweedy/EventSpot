import React from 'react';
import { FaSignOutAlt } from 'react-icons/fa';

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
        <button onClick={handleLogout} className="logout-button">
            <FaSignOutAlt />
            <p id="logout-button-text">Logout</p>
        </button>
        );
}

export default Logout;
